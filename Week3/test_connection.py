import os
import anthropic
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize the Anthropic client
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def test_chat():
    print("Testing Chatbot Connectivity...")
    messages = [{"role": "user", "content": "Hello! Just checking if you are working."}]
    
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=messages
        )
        ai_response = response.content[0].text
        print(f"AI Response: {ai_response}")
        print("SUCCESS: Chatbot is working correctly!")
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    test_chat()
