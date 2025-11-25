import httpx
import json
import os
from config import GEMINI_API_KEY

def test_gemini():
    if not GEMINI_API_KEY:
        print("Skipping Gemini test: No API key provided.")
        return

    # User provided example: gemini-2.5-flash-lite
    # URL: https://aiplatform.googleapis.com/v1/publishers/google/models/gemini-2.5-flash-lite:streamGenerateContent?key=${API_KEY}
    
    model = "gemini-2.5-flash-lite"
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
    
    print(f"Testing URL: {url.split('?')[0]}...") # Don't print key
    
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
    test_gemini()
