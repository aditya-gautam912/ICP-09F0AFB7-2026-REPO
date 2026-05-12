# Week 5: Advanced RAG Development (Multi-Document & Hybrid Search)

## Project Overview: Advanced Document Q&A
Enhanced version of the RAG system featuring multi-document support, hybrid retrieval (Vector + Keyword search), and Cross-Encoder re-ranking for superior accuracy.

## Key Features (Week 5 Refinement)
- [x] **Multi-Document Support:** Upload and index multiple PDFs with source metadata tracking.
- [x] **Hybrid Search:** Combines semantic vector search (ChromaDB) with keyword-based retrieval (BM25) using an `EnsembleRetriever`.
- [x] **Advanced Re-ranking:** Integrated `CrossEncoderReranker` (ms-marco-MiniLM) to prioritize the most relevant chunks after initial retrieval.
- [x] **Source Citation:** The assistant now cites specific documents in its answers and provides a list of sources.
- [x] **Polished UI Pro:** Professional Streamlit interface with:
    - Dual-column layout (Document Manager vs. Research Assistant).
    - Real-time indexing status using `st.status`.
    - **Source Explorer:** Inspect the exact context chunks used for each answer.
    - System diagnostics and chat history management.
- [x] **Persistence:** Vector store persists to `./chroma_db_week5`.

## 🖼️ Visual Preview
![RAG System Screenshot](Screenshot%202026-05-12%20170155.png)

## Tools & Libraries
- **Language:** Python
- **Framework:** LangChain (Classic & Core)
- **Vector Store:** ChromaDB
- **Keyword Search:** BM25 (Rank-BM25)
- **Re-ranker:** Sentence-Transformers (Cross-Encoder)
- **LLM:** Groq (Llama 3.3 70B)
- **UI:** Streamlit
