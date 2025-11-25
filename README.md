# WalletGenie 🧞‍♂️

WalletGenie is an AI-powered savings advisor built  It analyzes your bank statements (CSV) and helps you plan your savings using Gemini.

## ✨ Key Features

### Multi-Agent Architecture
WalletGenie uses a **three-agent system** built on Gemini 2.5 Pro:

1. **Transaction Normaliser** - Cleans CSV data, infers categories, and analyzes recent spending
2. **Insight Agent** - Finds patterns, anomalies, recurring payments, and calculates financial health score
3. **Savings Strategist** - Creates personalized saving plans with concrete steps (e.g., "Cut Dining by 15% → save $200")

### Financial Health Score (0-100)
A unique metric based on:
- **Savings Rate**: % of income saved
- **Fixed vs Variable Ratio**: Balance between fixed costs (housing, utilities) and variable spending
- **Spending Patterns**: Weekend overspend detection

The agent explains your score and provides actionable steps to improve it.

### Goal Simulation
Ask: "I want to save $5000 in 6 months. What should I change?"
WalletGenie will:
- Analyze your current spending
- Calculate required monthly savings
- Suggest category-specific cuts with projected savings
- Create a month-by-month action plan

### Conversation Memory
The agent maintains context across messages, creating a natural conversational experience where it remembers previous requests and builds on them.

## 🚀 Quick Start (Local)

### Prerequisites
- Node.js & npm
- Python 3.9+
- Google Cloud Project with Gemini API Key

### 1. Setup Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file in `backend/`:
```
PROJECT_ID=your-project-id
GCS_BUCKET=your-bucket-name
SQL_CONNECTION=sqlite:///./wallet.db # Local DB
GEMINI_API_KEY=your-gemini-api-key
```

### 2. Setup Frontend
```bash
cd frontend
npm install
```

### 3. Run Locally
We provide a helper script to run both services:
```bash
./run_locally.sh
```
Or run them separately:
- Backend: `cd backend && uvicorn main:app --reload --port 8080`
- Frontend: `cd frontend && ng serve`

Access the app at `http://localhost:4200`.

## ☁️ Deployment (Google Cloud Run)

### Architecture
For the hackathon (low cost), we deploy a **single Cloud Run service** that serves both the FastAPI backend and the Angular frontend (as static files).

### Steps
Use the provided deployment script:
```bash
./deploy.sh
```

Or manually:
1. **Build Frontend**:
   ```bash
   cd frontend
   npx ng build
   ```
   This creates `dist/frontend/browser`.

2. **Prepare Backend**:
   Ensure `main.py` is configured to serve static files from `../frontend/dist/frontend/browser`.

3. **Deploy**:
   ```bash
   # Submit build to Cloud Build
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/walletgenie

   # Deploy to Cloud Run
   gcloud run deploy walletgenie \
     --image gcr.io/YOUR_PROJECT_ID/walletgenie \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GEMINI_API_KEY=your-key
   ```

## 📊 Sample Data
Generate 12 months of transaction data for testing:
```bash
python3 generate_data.py
```

This creates `transactions_12months.csv` with realistic spending patterns across multiple categories.

## 💬 Sample Questions
Try these questions (see `sample_questions.md`):
- "What is my financial health score?"
- "I want to save $5000 in 6 months. What should I change?"
- "Did I overspend on weekends?"
- "Create a savings goal for a vacation"

## 🛠 Tech Stack
- **Frontend**: Angular 19
- **Backend**: FastAPI (Python)
- **Database**: Cloud SQL (PostgreSQL) / SQLite (Local)
- **AI**: Google Gemini 2.5 Pro (Vertex AI)
- **Multi-Agent System**: Custom implementation using Gemini function calling and system instructions

