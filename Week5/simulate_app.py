import os
import sys
import tempfile
import shutil
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import RAGEngine

load_dotenv()

def simulate_streamlit_process():
    print("--- Streamlit Logic Simulation ---")
    
    # 1. Setup Engine
    engine = RAGEngine()
    
    # 2. Source PDF
    source_pdf = r"C:\Users\ag950\Downloads\Assignment-5.pdf"
    if not os.path.exists(source_pdf):
        print(f"Error: Source PDF not found at {source_pdf}")
        return

    # 3. Simulate Streamlit's temporary file handling
    print(f"Simulating upload of: {os.path.basename(source_pdf)}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copy2(source_pdf, tmp.name)
        tmp_path = tmp.name
    
    print(f"Temporary file created at: {tmp_path}")

    # 4. Process PDF
    try:
        print("Calling engine.process_pdfs()...")
        num_chunks = engine.process_pdfs([tmp_path])
        
        if num_chunks > 0:
            print(f"Success! Created {num_chunks} chunks.")
            # 5. Test Query
            print("Testing Query...")
            answer = engine.get_answer("What is this document about?")
            print(f"Answer: {answer[:100]}...")
        else:
            print(f"Failure! Error reported by engine: {engine.last_error}")
            
    except Exception as e:
        print(f"Critical Exception: {e}")
    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            print("Temporary file cleaned up.")

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    simulate_streamlit_process()
