import httpx
import json
import os
from config import GEMINI_API_KEY

def test_gemini_pro():
    if not GEMINI_API_KEY:
        print("Skipping Gemini test: No API key provided.")
        return

    # Testing gemini-2.5-pro
    model = "gemini-2.5-pro"
    url = f"https://aiplatform.googleapis.com/v1/publishers/google/models/{model}:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": "Hello, are you there?"}]
            }
        ]
    }
    
    print(f"Testing URL: {url.split('?')[0]}...")
    
    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error Response:", response.text)
    except Exception as e:
        print(f"Request Failed: {e}")

if __name__ == "__main__":
    test_gemini_pro()
