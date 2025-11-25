from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from database import Transaction, Goal
from typing import Dict, Any, List
import datetime

def get_summary_data(db: Session) -> Dict[str, Any]:
    """
    Calculates summary metrics from transactions including a detailed health score.
    """
    # 1. Total Spend
    total_spend = db.query(func.sum(Transaction.amount)).filter(Transaction.type == 'debit').scalar() or 0.0
    
    # 2. Spend by Category
    category_spend = db.query(Transaction.category, func.sum(Transaction.amount)).\
        filter(Transaction.type == 'debit').\
        group_by(Transaction.category).\
        order_by(func.sum(Transaction.amount).desc()).all()
    
    top_categories = [{"category": cat, "amount": amt} for cat, amt in category_spend[:3]]
    
    # 3. Financial Health Score Calculation
    # Factors:
    # A. Savings Rate (Simulated: Assume Income = Total Spend * 1.2 for demo)
    assumed_income = total_spend * 1.2 if total_spend > 0 else 5000
    savings = assumed_income - total_spend
    savings_rate = (savings / assumed_income) * 100 if assumed_income > 0 else 0
    
    # B. Fixed vs Variable (Simulated: Housing/Utilities = Fixed, others Variable)
    fixed_cats = ['Housing', 'Utilities', 'Insurance', 'Rent']
    fixed_spend = sum(amt for cat, amt in category_spend if cat in fixed_cats)
    variable_spend = total_spend - fixed_spend
    fixed_ratio = (fixed_spend / total_spend) * 100 if total_spend > 0 else 0
    
    # C. Weekend Overspend (Simulated: Check if weekend spend > 40% of total)
    # Note: In a real app, we'd parse dates. For hackathon, we'll use a heuristic or random factor if dates aren't real objects.
    # We will skip complex date parsing for now to avoid errors if date format varies.
    
    # Score Logic (0-100)
    # Start at 50
    score = 50
    
    # Savings impact (+/- 20)
    if savings_rate > 20: score += 20
    elif savings_rate > 10: score += 10
    elif savings_rate < 0: score -= 10
    
    # Fixed ratio impact (+/- 10)
    if 30 <= fixed_ratio <= 50: score += 10 # Healthy fixed cost ratio
    elif fixed_ratio > 60: score -= 10 # High fixed costs
    
    # Cap score
    health_score = max(0, min(100, int(score)))
    
    return {
        "total_spend": total_spend,
        "top_categories": top_categories,
        "health_score": health_score,
        "insights": {
            "savings_rate": f"{savings_rate:.1f}%",
            "fixed_ratio": f"{fixed_ratio:.1f}%",
            "message": "Good savings rate!" if savings_rate > 10 else "Try to save at least 10% of income."
        }
    }

def get_recent_transactions_data(db: Session, limit: int = 5) -> List[Dict[str, Any]]:
    """Fetches recent transactions for the agent context."""
    rows = db.query(Transaction).order_by(Transaction.id.desc()).limit(limit).all()
    return [{
        "date": r.date,
        "description": r.description,
        "amount": r.amount,
        "category": r.category
    } for r in rows]

def create_new_goal(db: Session, target: float, months: int) -> Goal:
    goal = Goal(target_amount=target, months=months, created_at="2024-05-20")
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal
