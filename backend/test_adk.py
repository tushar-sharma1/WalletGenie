import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Force local SQLite for testing
if "SQL_CONNECTION" in os.environ:
    del os.environ["SQL_CONNECTION"]

from agent import chat_with_agent
from database import init_db

def test_agent():
    print("Initializing DB...")
    init_db()
    
    print("Testing Chat with Agent...")
    response = chat_with_agent("Hello! Who are you?")
    print(f"Response: {response}")
    
    response = chat_with_agent("What is my wallet summary?")
    print(f"Response: {response}")

if __name__ == "__main__":
    test_agent()
