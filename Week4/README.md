# Week 4: Project 2 Development (Document Q&A System)

## Project Overview: Document Q&A System (RAG)
A Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents and ask questions based on their content.

## Key Features (Week 4 Focus)
- [ ] PDF text extraction and chunking.
- [ ] Vector embeddings storage using ChromaDB.
- [ ] Retrieval-Augmented Generation (RAG) logic.
- [ ] Basic Streamlit interface for file upload and querying.

## Tools & Libraries
- **Language:** Python
- **Framework:** LangChain
- **Vector Store:** ChromaDB
- **LLM:** Groq (Llama 3)
- **UI:** Streamlit

## Technical Notes
- **Architecture Design:** Implemented a classic RAG pipeline: `Document -> Splitting -> Embeddings -> Vector Store -> Retrieval -> LLM`.
- **Advanced Patterns:** Utilized LangChain's Expression Language (LCEL) for building a modular and readable RAG chain.
- **Embeddings:** Used `HuggingFaceEmbeddings` with the `all-MiniLM-L6-v2` model for locally-processed semantic vectors.
- **Storage:** Configured ChromaDB as an in-memory vector database for the development phase.

## Current Progress
- [x] Project Initialization
- [x] Environment Setup
- [x] PDF Loading & Chunking
- [x] Vector Store Implementation
- [x] RAG Chain Setup
- [x] Streamlit UI Development
