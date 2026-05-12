import os
from rag_engine import RAGEngine
from dotenv import load_dotenv

# Load API keys
load_dotenv()

def test_rag():
    # Use a PDF from the downloads or a known path
    test_pdf = r"C:\Users\ag950\Downloads\Assignment-5.pdf"
    
    if not os.path.exists(test_pdf):
        print(f"Test PDF not found at {test_pdf}")
        return

    print("Initializing RAG Engine...")
    engine = RAGEngine(model_provider="groq")
    
    print(f"Processing {test_pdf}...")
    num_chunks = engine.process_pdf(test_pdf)
    print(f"Created {num_chunks} chunks.")
    
    query = "What is the main topic of this assignment?"
    print(f"Query: {query}")
    
    try:
        answer = engine.get_answer(query)
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"Error during Q&A: {e}")

if __name__ == "__main__":
    test_rag()
