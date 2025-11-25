import requests
import io
import json

BASE_URL = "http://localhost:8080"

def test_flow():
    print("Starting End-to-End Verification...")
    
    # 1. Upload CSV
    csv_content = """date,description,amount,category
2024-01-01,Uber,-15.00,Transport
2024-01-02,Starbucks,-5.50,Food
2024-01-03,Rent,-1200.00,Housing
2024-01-04,Grocery,-45.00,Food
2024-01-05,Netflix,-12.00,Entertainment
"""
    files = {'file': ('test.csv', csv_content, 'text/csv')}
    try:
        # Note: This requires the server to be running. 
        # Since I cannot run the server in background easily and query it in the same script without complex setup in this env,
        # I will simulate the calls by importing the app directly if possible, or just assume this script is for the user to run.
        # BUT, I can import the functions from main.py and test them directly!
        
        from main import app, upload_csv, get_summary, chat, ChatRequest
        from database import init_db, get_db, SessionLocal
        from fastapi.testclient import TestClient
        
        # Initialize DB
        init_db()
        
        client = TestClient(app)
        
        # Upload
        print("\nTesting /upload...")
        response = client.post("/upload", files={"file": ("test.csv", csv_content, "text/csv")})
        print("Upload Response:", response.json())
        assert response.status_code == 200
        
        # Summary
        print("\nTesting /summary...")
        response = client.get("/summary")
        print("Summary Response:", response.json())
        assert response.status_code == 200
        assert response.json()['total_spend'] > 0
        
        # Chat (Mocking Gemini if no key)
        print("\nTesting /chat...")
        # If no API key, this might fail or print error.
        # We'll try a simple message.
        response = client.post("/chat", json={"message": "How much did I spend on Food?"})
        print("Chat Response:", response.json())
        
        print("\nVerification Successful!")
        
    except Exception as e:
        print(f"\nVerification Failed: {e}")

if __name__ == "__main__":
    # Ensure we are in backend dir or path is set
    import sys
    import os
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    test_flow()
