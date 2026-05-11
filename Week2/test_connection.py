import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def test_chat():
    print("Testing Llama 3 Chatbot Connectivity...")
    messages = [
        {"role": "system", "content": "You are a helpful and intelligent AI assistant."},
        {"role": "user", "content": "Hello! Just checking if you are working."}
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=50,
            temperature=0.7,
            stream=False
        )
        ai_response = response.choices[0].message.content
        print(f"AI Response: {ai_response}")
        print("SUCCESS: Chatbot is working correctly!")
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    test_chat()
