import os
from rag_engine import RAGEngine
from dotenv import load_dotenv

load_dotenv()

def test_week5_features():
    print("--- Week 5 Feature Test ---")
    
    # Files to test
    pdf1 = r"C:\Users\ag950\Downloads\Assignment-5.pdf"
    pdf2 = r"C:\Users\ag950\Downloads\App Development_Task.pdf"
    
    engine = RAGEngine()
    
    # 1. Test Multi-Doc Processing
    print(f"\nProcessing Multi-Docs...")
    paths = [p for p in [pdf1, pdf2] if os.path.exists(p)]
    if not paths:
        print("[ERROR] No test PDFs found.")
        return
        
    num_chunks = engine.process_pdfs(paths)
    print(f"[OK] Processed {len(paths)} files. Total chunks: {len(engine.all_chunks)}")

    # 2. Test Hybrid Retrieval
    print("\nTesting Hybrid Search (Vector + BM25)...")
    query = "List the main database tasks and the app development requirements."
    print(f"Query: {query}")
    
    try:
        answer = engine.get_answer(query)
        print(f"\n[OK] Hybrid Answer:\n{answer}")
    except Exception as e:
        print(f"[ERROR] Answer generation failed: {e}")

if __name__ == "__main__":
    test_week5_features()
