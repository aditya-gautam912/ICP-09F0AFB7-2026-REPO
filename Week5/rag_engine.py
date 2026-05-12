import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.retrievers import BM25Retriever

# Load environment variables
load_dotenv()

class RAGEngine:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        self.all_chunks = []
        self.compression_retriever = None
        self.last_error = None
        self.persist_directory = "./chroma_db_week5"
        
        # Initialize CrossEncoder for Re-ranking
        try:
            self.cross_encoder = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
            self.reranker = CrossEncoderReranker(model=self.cross_encoder, top_n=3)
        except Exception as e:
            print(f"Warning: Re-ranker failed to initialize: {e}")
            self.reranker = None

    def process_pdfs(self, file_paths, original_names=None):
        """Loads and chunks multiple PDF files with metadata refinement."""
        self.last_error = None
        
        if not file_paths:
            self.last_error = "No files provided for processing."
            return 0
            
        new_chunks = []
        
        for i, file_path in enumerate(file_paths):
            if not os.path.exists(file_path):
                print(f"DEBUG: File not found: {file_path}")
                continue
            try:
                loader = PyPDFLoader(file_path)
                pages = loader.load()
                
                # Override metadata source with original name if provided
                source_name = original_names[i] if original_names and i < len(original_names) else os.path.basename(file_path)
                
                if not pages:
                    print(f"DEBUG: No pages in {source_name}")
                    continue
                
                for page in pages:
                    page.metadata["source"] = source_name
                
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=800,
                    chunk_overlap=100
                )
                chunks = text_splitter.split_documents(pages)
                new_chunks.extend(chunks)
            except Exception as e:
                self.last_error = f"Error reading {os.path.basename(file_path)}: {str(e)}"
                print(f"DEBUG: {self.last_error}")
                return 0
        
        if not new_chunks:
            self.last_error = "No text chunks were generated from the provided files."
            return 0

        self.all_chunks.extend(new_chunks)
        
        try:
            # Persistent Vector Store - Ensure we handle potential lock issues
            if self.vector_store:
                # Add to existing store
                self.vector_store.add_documents(new_chunks)
            else:
                self.vector_store = Chroma.from_documents(
                    documents=self.all_chunks,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory
                )
            
            # Rebuild Retrievers
            bm25_retriever = BM25Retriever.from_documents(self.all_chunks)
            bm25_retriever.k = 5
            
            self.ensemble_retriever = EnsembleRetriever(
                retrievers=[self.vector_store.as_retriever(search_kwargs={"k": 5}), bm25_retriever],
                weights=[0.6, 0.4]
            )
            
            # Advanced Retrieval: Re-ranking
            if self.reranker:
                self.compression_retriever = ContextualCompressionRetriever(
                    base_compressor=self.reranker, 
                    base_retriever=self.ensemble_retriever
                )
            else:
                self.compression_retriever = self.ensemble_retriever
                
            return len(new_chunks)
        except Exception as e:
            self.last_error = f"Error building search index: {str(e)}"
            print(f"DEBUG: {self.last_error}")
            return 0

    def format_docs(self, docs):
        formatted = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "Unknown")
            formatted.append(f"--- Document {i+1} (Source: {source}) ---\n{doc.page_content}")
        return "\n\n".join(formatted)

    def get_answer(self, query):
        """Retrieves context using Advanced Hybrid Search + Re-ranking."""
        if not self.compression_retriever:
            return "Knowledge base not ready. Please upload a valid PDF.", []

        template = """You are an elite research assistant. Use the provided context to answer the question.
        
        Guidelines:
        1. Base your answer ONLY on the context.
        2. If multiple documents are provided, synthesize information across them.
        3. Cite the source (e.g., 'According to Document.pdf...') if possible.
        4. If the answer is missing, state clearly that you don't know.

        Context:
        {context}

        Question: {question}
        
        Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)

        try:
            # We use invoke on the retriever to get docs for possible source extraction later
            docs = self.compression_retriever.invoke(query)
            context_text = self.format_docs(docs)
            
            rag_chain = (
                prompt
                | self.llm
                | StrOutputParser()
            )
            
            response = rag_chain.invoke({"context": context_text, "question": query})
            
            # Append sources to the response for UI (keeping it simple for now)
            sources = set(doc.metadata.get("source", "Unknown") for doc in docs)
            source_list = ", ".join(sources)
            full_response = f"{response}\n\n**Sources:** {source_list}"
            
            return full_response, docs
            
        except Exception as e:
            error_msg = str(e)
            if "rate_limit_exceeded" in error_msg.lower():
                return "Error: Groq API Rate limit reached. Please wait a minute and try again.", []
            return f"Error generating answer: {e}", []

if __name__ == "__main__":
    pass

