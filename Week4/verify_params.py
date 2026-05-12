import os
from rag_engine import RAGEngine
from dotenv import load_dotenv

# Load API keys
load_dotenv()

def verify_parameters():
    test_pdf = r"C:\Users\ag950\Downloads\Assignment-5.pdf"
    
    print("--- Starting Parameter Verification (Groq-Only) ---")
    
    # 1. Check File Existence
    if not os.path.exists(test_pdf):
        print(f"[ERROR] Test PDF not found: {test_pdf}")
        return
    print(f"[OK] Test PDF found: {test_pdf}")

    # 2. Check API Keys
    groq_key = os.getenv("GROQ_API_KEY")
    
    if groq_key:
        print("[OK] GROQ_API_KEY is configured.")
    else:
        print("[ERROR] GROQ_API_KEY is missing.")
        return

    # 3. Test RAG Engine with Groq
    print("\n--- Testing RAG Engine (Groq) ---")
    try:
        engine = RAGEngine()
        num_chunks = engine.process_pdf(test_pdf)
        print(f"[OK] PDF Chunking successful: {num_chunks} chunks created.")
        
        query = "What are the specific tasks mentioned in this document?"
        print(f"Testing Query: {query}")
        answer = engine.get_answer(query)
        if answer and len(answer) > 10:
            print(f"[OK] Answer received: {answer[:100]}...")
        else:
            print("[ERROR] Answer was too short or empty.")
    except Exception as e:
        print(f"[ERROR] Groq Test Failed: {e}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify_parameters()
