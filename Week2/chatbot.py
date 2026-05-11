import os
import anthropic
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize the Anthropic client
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def chat():
    print("--- AI Chatbot (Type 'quit' to exit) ---")
    
    # Store conversation history
    messages = []
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("AI: Goodbye!")
            break
            
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Generate response from Claude
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=messages
            )
            
            # Extract and print the response
            ai_response = response.content[0].text
            print(f"AI: {ai_response}")
            
            # Add AI response to history
            messages.append({"role": "assistant", "content": ai_response})
            
        except anthropic.APIConnectionError as e:
            print("Error: The server could not be reached. Check your internet connection.")
        except anthropic.RateLimitError as e:
            print("Error: A 429 status code was received; we should back off a bit.")
        except anthropic.APIStatusError as e:
            print(f"Error: Another non-200-range status code was received: {e.status_code}")
            print(e.response)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    chat()
