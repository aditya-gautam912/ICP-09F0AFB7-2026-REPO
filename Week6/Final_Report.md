# Final Internship Report - Generative AI Development

**Intern:** Aditya Gautam
**Portal ID:** ICP-09F0AFB7-2026
**Period:** April 2026 - May 2026

## Executive Summary
Over the course of this 6-week internship, I have developed a deep practical understanding of the Generative AI lifecycle. I successfully transitioned from building basic LLM-integrated chatbots to architecting advanced Retrieval-Augmented Generation (RAG) systems. Key technologies mastered include LangChain, ChromaDB, Groq Inference Engine, and sophisticated retrieval strategies like Hybrid Search and Cross-Encoder Re-ranking.

## Project 1: Intelligent Chatbot (Groq/Llama)
### Technical Overview
- **LLM:** Groq (Llama 3.3 70B)
- **Stack:** Python, Streamlit
- **Key Achievements:**
    - Developed a low-latency conversational interface using the Groq Inference Engine.
    - Implemented robust session-state management to maintain chat history.
    - Designed a clean, user-friendly UI using Streamlit with custom CSS.

### Challenges & Solutions
- **Challenge:** Maintaining context in long conversations.
- **Solution:** Implemented a rolling message history buffer passed to the LLM in each turn, ensuring the assistant "remembers" previous user inputs.

## Project 2: Advanced Multi-Document RAG System
### Technical Overview
- **LLM:** Groq (Llama 3.3 70B)
- **Vector Database:** ChromaDB
- **Retrieval:** Hybrid Search (BM25 + Vector) + Cross-Encoder Re-ranking
- **Stack:** LangChain, Streamlit

### Key Achievements
- **Multi-Doc Support:** Engineered a pipeline to handle multiple PDF uploads with automatic source metadata tagging.
- **Advanced Retrieval:** Implemented an Ensemble Retriever combining semantic (ChromaDB) and keyword (BM25) search.
- **Re-ranking:** Integrated a Cross-Encoder model (`ms-marco-MiniLM`) to refine retrieval results, significantly improving answer precision.
- **Source Explorer:** Developed a UI feature to allow users to inspect the exact context chunks used for each AI response.

### Challenges & Solutions
- **Challenge:** Handling high-volume PDF processing and vector store locks.
- **Solution:** Refined the indexing logic to use persistent storage and incremental updates, preventing system crashes during multi-file uploads.

## Visual Gallery

### Project 1: Intelligent Chatbot
![Project 1 Screenshot](../Week3/Screenshot%202026-05-12%20171019.png)

### Project 2: Advanced RAG System
![Project 2 Screenshot](../Week5/Screenshot%202026-05-12%20170155.png)

## Learning Outcomes
- Advanced proficiency in the RAG (Retrieval-Augmented Generation) architecture.
- Practical experience with Vector Databases (ChromaDB) and hybrid search strategies.
- Mastery of Prompt Engineering and system message optimization for Llama 3 models.
- Understanding of the importance of metadata in document retrieval and citation.

## Conclusion
This internship provided a rigorous environment to apply theoretical GenAI concepts to real-world problems. By building functional applications from the ground up, I have gained the confidence and technical skills necessary to contribute to professional AI development teams.
