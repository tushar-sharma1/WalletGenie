from agent import chat_with_agent

def test_agent():
    print("Testing Agent with REST implementation...")
    
    # Test 1: Simple Chat
    print("\n1. Simple Chat:")
    res = chat_with_agent("Hello, who are you?")
    print(f"Response: {res}")
    
    # Test 2: Tool Call (Summary)
    # Note: Requires DB to have data. If empty, it might return 0s.
    print("\n2. Tool Call (Summary):")
    res = chat_with_agent("What is my financial health score?")
    print(f"Response: {res}")

if __name__ == "__main__":
    test_agent()
