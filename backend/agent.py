import httpx
import json
import os
from config import GEMINI_API_KEY
from database import SessionLocal, Transaction, Goal
from services import get_summary_data, create_new_goal, get_recent_transactions_data
from sqlalchemy import func

# --- Tool Implementations ---

def get_wallet_summary():
    """
    Retrieves the current wallet summary including total spend, top categories, and financial health score.
    Returns JSON string.
    """
    db = SessionLocal()
    try:
        data = get_summary_data(db)
        return json.dumps(data)
    finally:
        db.close()

def get_recent_transactions(limit: int = 5):
    """
    Retrieves the most recent transactions.
    Args:
        limit: Number of transactions to return (default 5).
    Returns JSON string.
    """
    db = SessionLocal()
    try:
        data = get_recent_transactions_data(db, limit)
        return json.dumps(data)
    finally:
        db.close()

def simulate_savings(goal_amount: float, months: int):
    """
    Simulates a savings plan. Calculates required monthly savings and suggests category cuts.
    Args:
        goal_amount: The target amount to save.
        months: The number of months to achieve the goal.
    Returns JSON string with plan.
    """
    db = SessionLocal()
    try:
        required_monthly = float(goal_amount) / int(months)
        
        # Get top spending categories to suggest cuts
        category_spend = db.query(Transaction.category, func.sum(Transaction.amount)).\
            filter(Transaction.type == 'debit').\
            group_by(Transaction.category).\
            order_by(func.sum(Transaction.amount).desc()).all()
        
        suggestions = []
        for cat, amt in category_spend[:3]:
            cut_amount = amt * 0.2
            suggestions.append(f"Cut {cat} spending by {cut_amount:.2f} (20%)")
            
        return json.dumps({
            "required_monthly_savings": required_monthly,
            "suggestions": suggestions,
            "message": f"To save {goal_amount} in {months} months, you need to save {required_monthly:.2f}/month."
        })
    finally:
        db.close()

def create_savings_goal(target_amount: float, months: int):
    """
    Creates a new savings goal in the database.
    Args:
        target_amount: The target amount.
        months: Timeframe in months.
    """
    db = SessionLocal()
    try:
        goal = create_new_goal(db, float(target_amount), int(months))
        return json.dumps({"status": "success", "goal_id": goal.id, "message": "Goal created successfully."})
    finally:
        db.close()

# --- Tool Definitions (Schema) ---

tools_schema = [
    {
        "function_declarations": [
            {
                "name": "get_wallet_summary",
                "description": "Retrieves the current wallet summary including total spend, top categories, and health score.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {},
                }
            },
            {
                "name": "get_recent_transactions",
                "description": "Retrieves the most recent transactions to find patterns or anomalies.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "limit": {"type": "INTEGER", "description": "Number of transactions to return."}
                    },
                }
            },
            {
                "name": "simulate_savings",
                "description": "Simulates a savings plan. Calculates required monthly savings and suggests category cuts.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "goal_amount": {"type": "NUMBER", "description": "The target amount to save."},
                        "months": {"type": "INTEGER", "description": "The number of months to achieve the goal."}
                    },
                    "required": ["goal_amount", "months"]
                }
            },
            {
                "name": "create_savings_goal",
                "description": "Creates a new savings goal in the database.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "target_amount": {"type": "NUMBER", "description": "The target amount."},
                        "months": {"type": "INTEGER", "description": "Timeframe in months."}
                    },
                    "required": ["target_amount", "months"]
                }
            }
        ]
    }
]

# --- Agent Logic ---

MODEL_NAME = "gemini-2.5-pro"
BASE_URL = f"https://aiplatform.googleapis.com/v1/publishers/google/models/{MODEL_NAME}:generateContent"

SYSTEM_INSTRUCTION = """
You are WalletGenie, an advanced Multi-Agent Financial Assistant.
You are composed of three specialized sub-agents:

1. **Transaction Normaliser**: You understand transaction data. Use `get_recent_transactions` to look at actual data rows.
2. **Insight Agent**: You analyze spending patterns and financial health. Use `get_wallet_summary` to get the health score. Explain the score clearly (e.g., "Your score is 62/100 because...").
3. **Savings Strategist**: You help users achieve goals. Use `simulate_savings` to create actionable plans.

**Guidelines:**
- **Be Proactive**: Offer insights. If the health score is low, suggest improvements.
- **Be Specific**: Quote actual amounts and dates from the data.
- **Be Action-Oriented**: Give step-by-step plans.
"""

# Conversation history storage (in-memory for demo)
conversation_history = {}

def chat_with_agent(user_message: str, session_id: str = "default"):
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is not set."

    url = f"{BASE_URL}?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # Initialize or get conversation history for this session
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    
    # Add user message to history
    conversation_history[session_id].append({
        "role": "user",
        "parts": [{"text": user_message}]
    })
    
    # Build payload with full conversation history
    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        "contents": conversation_history[session_id],
        "tools": tools_schema
    }
    
    try:
        # 1. Send User Message
        response = httpx.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            return f"Error from Gemini: {response.text}"
            
        resp_json = response.json()
        
        # Check for function call
        try:
            candidate = resp_json['candidates'][0]
            parts = candidate['content']['parts']
            function_call = next((p['functionCall'] for p in parts if 'functionCall' in p), None)
        except (KeyError, IndexError):
            return "Error parsing response."

        if function_call:
            # 2. Execute Function
            fn_name = function_call['name']
            fn_args = function_call['args']
            
            print(f"Agent calling function: {fn_name} with {fn_args}")
            
            result = "{}"
            if fn_name == "get_wallet_summary":
                result = get_wallet_summary()
            elif fn_name == "get_recent_transactions":
                result = get_recent_transactions(fn_args.get('limit', 5))
            elif fn_name == "simulate_savings":
                result = simulate_savings(fn_args.get('goal_amount'), fn_args.get('months'))
            elif fn_name == "create_savings_goal":
                result = create_savings_goal(fn_args.get('target_amount'), fn_args.get('months'))
            
            # Add model's function call to history
            conversation_history[session_id].append({
                "role": "model",
                "parts": [{"functionCall": function_call}]
            })
            
            # Add function response to history
            conversation_history[session_id].append({
                "role": "function",
                "parts": [{
                    "functionResponse": {
                        "name": fn_name,
                        "response": {"name": fn_name, "content": json.loads(result)} 
                    }
                }]
            })
            
            # 3. Send Function Response back to model
            payload_2 = {
                "system_instruction": {
                    "parts": [{"text": SYSTEM_INSTRUCTION}]
                },
                "contents": conversation_history[session_id],
                "tools": tools_schema
            }
            
            response_2 = httpx.post(url, headers=headers, json=payload_2, timeout=30)
            if response_2.status_code != 200:
                return f"Error after function call: {response_2.text}"
                
            resp_json_2 = response_2.json()
            try:
                text_response = resp_json_2['candidates'][0]['content']['parts'][0]['text']
                # Add final text response to history
                conversation_history[session_id].append({
                    "role": "model",
                    "parts": [{"text": text_response}]
                })
                return text_response
            except:
                return "Agent executed action but returned no text."

        else:
            # Just text response
            try:
                text_response = parts[0]['text']
                # Add model's text response to history
                conversation_history[session_id].append({
                    "role": "model",
                    "parts": [{"text": text_response}]
                })
                return text_response
            except:
                return "No text response."

    except Exception as e:
        return f"System Error: {str(e)}"
