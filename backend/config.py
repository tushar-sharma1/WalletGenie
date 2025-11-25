import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

PROJECT_ID = os.getenv("PROJECT_ID", "walletgenie-hackathon")
GCS_BUCKET = os.getenv("GCS_BUCKET", "walletgenie-bucket")
SQL_CONNECTION = os.getenv("SQL_CONNECTION", "walletgenie-sql")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set.")
