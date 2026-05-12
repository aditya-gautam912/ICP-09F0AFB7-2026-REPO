import streamlit as st
import os
import tempfile
from rag_engine import RAGEngine

# Page config
st.set_page_config(page_title="DocQ&A - Project 2", page_icon="📄")

st.title("📄 Document Q&A System (RAG)")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    st.info("Using Groq (Llama 3) for optimized performance.")
    st.info("Ensure your GROQ_API_KEY is set in the .env file.")

# Initialize RAG Engine
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

# File Upload
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
        with st.spinner("Processing PDF..."):
            num_chunks = st.session_state.rag_engine.process_pdf(tmp_file_path)
            st.session_state.last_uploaded = uploaded_file.name
            st.success(f"PDF processed! Created {num_chunks} chunks.")
    
    # Clean up temp file
    os.remove(tmp_file_path)

st.markdown("---")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask a question about the document:"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.rag_engine.get_answer(prompt)
            st.markdown(response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
