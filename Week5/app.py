import streamlit as st
import os
import tempfile
import traceback
from rag_engine import RAGEngine

# Page config
st.set_page_config(page_title="Advanced DocQ&A Pro", page_icon="🚀", layout="wide")

# Custom CSS for a more polished look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stChatMessage { border-radius: 12px; margin-bottom: 1rem; }
    .st-emotion-cache-16idsys p { font-size: 1.1rem; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }
    h1 { color: #0f172a; font-weight: 800; }
    .source-tag { background-color: #e2e8f0; border-radius: 4px; padding: 2px 6px; font-size: 0.8rem; margin-right: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Advanced Multi-Document Q&A Pro")
st.caption("Week 5: Hybrid Search + Re-ranking + Multi-Doc Synthesis")
st.markdown("---")

# Initialize RAG Engine
if "rag_engine" not in st.session_state:
    with st.spinner("Initializing AI Engine..."):
        st.session_state.rag_engine = RAGEngine()
    st.session_state.processed_files = set()
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.header("⚙️ System Status")
    
    # Engine Stats
    stats_container = st.container(border=True)
    with stats_container:
        st.write(f"**Chunks:** {len(st.session_state.rag_engine.all_chunks)}")
        status_icon = "✅" if st.session_state.rag_engine.compression_retriever else "❌"
        st.write(f"**Engine:** {status_icon} Ready")
        
        if st.session_state.rag_engine.reranker:
            st.success("Re-ranking: Active")
        else:
            st.warning("Re-ranking: Inactive")

    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🔄 Reset Knowledge Base", use_container_width=True, type="secondary"):
        st.session_state.rag_engine = RAGEngine()
        st.session_state.processed_files = set()
        st.session_state.messages = []
        st.success("Knowledge base reset!")

# Main Layout
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("📤 Document Manager")
    uploaded_files = st.file_uploader(
        "Upload PDFs for analysis", 
        type="pdf", 
        accept_multiple_files=True,
        help="Upload multiple files to synthesize answers across them."
    )

    if uploaded_files:
        new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]
        
        if new_files:
            with st.status("Processing documents...", expanded=True) as status:
                temp_paths = []
                try:
                    st.write("Preparing temporary files...")
                    for f in new_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(f.getvalue())
                            temp_paths.append(tmp.name)
                    
                    st.write("Extracting text and generating embeddings...")
                    original_names = [f.name for f in new_files]
                    num_chunks = st.session_state.rag_engine.process_pdfs(temp_paths, original_names=original_names)
                    
                    if num_chunks > 0:
                        for f in new_files:
                            st.session_state.processed_files.add(f.name)
                        status.update(label=f"Successfully indexed {len(new_files)} documents!", state="complete", expanded=False)
                    else:
                        status.update(label="Indexing failed!", state="error", expanded=True)
                        st.error(st.session_state.rag_engine.last_error)
                
                except Exception as e:
                    status.update(label="Critical error during processing!", state="error", expanded=True)
                    st.error(f"Error: {str(e)}")
                    st.code(traceback.format_exc())
                finally:
                    for path in temp_paths:
                        if os.path.exists(path):
                            os.remove(path)

    if st.session_state.processed_files:
        with st.expander("📁 Managed Documents", expanded=True):
            for f_name in st.session_state.processed_files:
                st.write(f"📄 {f_name}")

with col2:
    st.subheader("💬 Research Assistant")
    
    # Chat container
    chat_container = st.container(height=500)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask anything about your documents..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing across documents..."):
                    response, docs = st.session_state.rag_engine.get_answer(prompt)
                    st.markdown(response)
                    
                    if docs:
                        with st.expander("🔍 View Retrieved Context"):
                            for i, doc in enumerate(docs):
                                st.markdown(f"**Chunk {i+1}** (Source: {doc.metadata.get('source', 'Unknown')})")
                                st.text(doc.page_content)
                                st.divider()
        
        st.session_state.messages.append({"role": "assistant", "content": response})
