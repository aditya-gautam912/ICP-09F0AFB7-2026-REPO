import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def chat():
    print("--- AI Chatbot (Groq/Llama3) - Type 'quit' to exit ---")
    
    # Store conversation history
    messages = [
        {
            "role": "system",
            "content": "You are a helpful and intelligent AI assistant."
        }
    ]
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("AI: Goodbye!")
            break
            
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Generate response from Groq using a supported Llama model
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
            )
            
            # Extract and print the response
            ai_response = completion.choices[0].message.content
            print(f"AI: {ai_response}")
            
            # Add AI response to history
            messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chat()
