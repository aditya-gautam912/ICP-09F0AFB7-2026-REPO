import os
import sys
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import RAGEngine

load_dotenv()

def verify_week5():
    print("--- Week 5 Advanced RAG Verification ---")
    
    # 1. Environment & Dependencies
    print("\n[1/5] Checking Environment:")
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print("  - GROQ_API_KEY: Found ✅")
    else:
        print("  - GROQ_API_KEY: Missing ❌")
        return

    try:
        from rank_bm25 import BM25Okapi
        from langchain_classic.retrievers import EnsembleRetriever
        print("  - Dependencies (BM25, LangChain-Classic): Loaded ✅")
    except ImportError as e:
        print(f"  - Dependencies: Error loading ({e}) ❌")
        return

    # 2. Initialization
    print("\n[2/5] Initializing Engine:")
    try:
        engine = RAGEngine()
        print("  - RAGEngine: Initialized ✅")
    except Exception as e:
        print(f"  - RAGEngine: Failed ({e}) ❌")
        return

    # 3. Multi-Document Processing
    print("\n[3/5] Testing Multi-Doc Processing:")
    test_files = [
        r"C:\Users\ag950\Downloads\Assignment-5.pdf",
        r"C:\Users\ag950\Downloads\App Development_Task.pdf"
    ]
    existing_files = [f for f in test_files if os.path.exists(f)]
    
    if not existing_files:
        print("  - Test Files: None found in Downloads. ⚠️")
    else:
        try:
            num_chunks = engine.process_pdfs(existing_files)
            print(f"  - Processing: {len(existing_files)} files, {num_chunks} new chunks ✅")
        except Exception as e:
            print(f"  - Processing: Failed ({e}) ❌")
            return

    # 4. Hybrid Retrieval Logic
    print("\n[4/5] Testing Hybrid Retrieval:")
    if not engine.ensemble_retriever:
        print("  - EnsembleRetriever: Not initialized (skip) ❌")
    else:
        try:
            # Test keyword match (BM25)
            bm25_results = engine.ensemble_retriever.retrievers[1].invoke("database")
            # Test vector match
            vector_results = engine.ensemble_retriever.retrievers[0].invoke("app requirements")
            print(f"  - Hybrid Search: Retrievers are active and returning docs ✅")
        except Exception as e:
            print(f"  - Hybrid Search: Failed retrieval test ({e}) ❌")

    # 5. End-to-End Generation
    print("\n[5/5] Testing Response Generation:")
    try:
        query = "Summarize the goals of the projects mentioned."
        # The new engine returns (answer, docs)
        result = engine.get_answer(query)
        if isinstance(result, tuple):
            answer, docs = result
        else:
            answer = result
            
        if answer and len(answer) > 20:
            print(f"  - Answer Generation: Success ✅")
            print(f"\nFinal Answer Snippet:\n{answer[:200]}...")
        else:
            print(f"  - Answer Generation: Fail (Length: {len(answer) if answer else 0}) ❌")
    except Exception as e:
        print(f"  - Answer Generation: Failed ({e}) ❌")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify_week5()
