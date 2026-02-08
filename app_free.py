import streamlit as st
import os
from pathlib import Path
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import chromadb

# Page configuration
st.set_page_config(
    page_title="Document Q&A with RAG (FREE)",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .upload-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def load_document(file_path, file_type):
    """Load document based on file type"""
    try:
        if file_type == "pdf":
            loader = PyPDFLoader(file_path)
        elif file_type == "txt":
            loader = TextLoader(file_path)
        elif file_type == "docx":
            loader = Docx2txtLoader(file_path)
        else:
            st.error(f"Unsupported file type: {file_type}")
            return None
        
        documents = loader.load()
        return documents
    except Exception as e:
        st.error(f"Error loading document: {str(e)}")
        return None

def process_documents(uploaded_files, model_name="llama3.2"):
    """Process uploaded documents and create vector store"""
    all_documents = []
    
    with st.spinner("📄 Loading documents..."):
        for uploaded_file in uploaded_files:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Determine file type
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Load document
            documents = load_document(tmp_file_path, file_extension)
            
            if documents:
                all_documents.extend(documents)
                st.success(f"✅ Loaded: {uploaded_file.name}")
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
    
    if not all_documents:
        st.error("No documents were successfully loaded.")
        return None, None
    
    # Split documents into chunks
    with st.spinner("✂️ Splitting documents into chunks..."):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_documents(all_documents)
        st.info(f"📊 Created {len(chunks)} text chunks from {len(all_documents)} documents")
    
    # Create embeddings and vector store
    with st.spinner("🧮 Creating embeddings and vector store (this may take a minute)..."):
        try:
            embeddings = OllamaEmbeddings(model=model_name)
            
            # Create persistent directory for ChromaDB
            persist_directory = "./chroma_db_free"
            
            # Create vector store
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=persist_directory
            )
            
            st.success("✅ Vector store created successfully!")
            return vectorstore, chunks
        except Exception as e:
            st.error(f"Error creating vector store: {str(e)}")
            st.error("Make sure Ollama is running with: ollama run llama3.2")
            return None, None

def create_qa_chain(vectorstore, model_name="llama3.2", temperature=0.7):
    """Create the QA chain with custom prompt"""
    
    # Custom prompt template
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Keep your answer concise and relevant.
    
    Context: {context}
    
    Question: {question}
    
    Helpful Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    
    # Create LLM
    llm = Ollama(
        model=model_name,
        temperature=temperature
    )
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    return qa_chain

def main():
    # Header
    st.title("📚 Document Q&A with RAG (FREE)")
    st.markdown("### Upload documents and ask questions - 100% Free, No API Key Needed!")
    
    # Check Ollama
    ollama_running = check_ollama()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Ollama status
        if ollama_running:
            st.success("✅ Ollama is running!")
        else:
            st.error("❌ Ollama is not running")
            st.markdown("""
            **To start Ollama:**
            1. Install: https://ollama.ai
            2. Run: `ollama run llama3.2`
            """)
        
        st.markdown("---")
        
        # Model selection
        model_name = st.selectbox(
            "Select Model",
            ["llama3.2", "llama3.2:1b", "mistral", "phi3"],
            help="Choose your local AI model"
        )
        
        st.markdown("---")
        
        # Temperature slider
        temperature = st.slider(
            "Response Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Lower values make responses more focused and deterministic"
        )
        
        st.markdown("---")
        
        # File upload
        st.header("📁 Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose files (PDF, TXT, DOCX)",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True,
            help="Upload one or more documents to create your knowledge base"
        )
        
        # Process button
        if uploaded_files and ollama_running:
            if st.button("🚀 Process Documents", type="primary"):
                vectorstore, chunks = process_documents(uploaded_files, model_name)
                
                if vectorstore:
                    st.session_state.vectorstore = vectorstore
                    st.session_state.qa_chain = create_qa_chain(vectorstore, model_name, temperature)
                    st.session_state.documents_loaded = True
                    st.session_state.chat_history = []
                    st.success("🎉 Ready to answer questions!")
                    st.rerun()
        
        elif uploaded_files and not ollama_running:
            st.warning("⚠️ Please start Ollama first")
        
        st.markdown("---")
        
        # Clear button
        if st.session_state.documents_loaded:
            if st.button("🗑️ Clear All"):
                st.session_state.vectorstore = None
                st.session_state.qa_chain = None
                st.session_state.chat_history = []
                st.session_state.documents_loaded = False
                st.rerun()
        
        # Info section
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This app is **100% FREE**:
        - **Ollama** for local AI
        - **LangChain** for RAG
        - **ChromaDB** for vectors
        - **No API costs!**
        """)
    
    # Main content area
    if not st.session_state.documents_loaded:
        # Welcome message
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if not ollama_running:
                st.warning("⚠️ Ollama is not running. Please start it first!")
                st.markdown("""
                ### 🚀 Quick Start:
                1. **Install Ollama**: https://ollama.ai
                2. **Run in terminal**: `ollama run llama3.2`
                3. **Upload documents** in the sidebar
                4. **Start asking questions!**
                """)
            else:
                st.info("👈 Upload documents in the sidebar to get started!")
            
            st.markdown("### 🎯 How it works:")
            st.markdown("""
            1. **Upload** your documents (PDF, TXT, or DOCX)
            2. **Process** them to create a searchable knowledge base
            3. **Ask** questions and get accurate answers with sources
            4. **100% FREE** - runs completely on your computer!
            """)
            
            st.markdown("### 📋 Example Questions:")
            st.markdown("""
            - What are the main topics covered in the document?
            - Can you summarize the key findings?
            - What does the document say about [specific topic]?
            - Who are the main people or entities mentioned?
            """)
    
    else:
        # Chat interface
        st.markdown("### 💬 Ask Questions About Your Documents")
        
        # Display chat history
        for i, (question, answer, sources) in enumerate(st.session_state.chat_history):
            with st.container():
                st.markdown(f"**❓ You:** {question}")
                st.markdown(f"**🤖 Assistant:** {answer}")
                
                if sources:
                    with st.expander("📄 View Sources"):
                        for j, source in enumerate(sources):
                            st.markdown(f"**Source {j+1}:**")
                            st.text(source.page_content[:300] + "...")
                            st.markdown(f"*Metadata:* {source.metadata}")
                
                st.markdown("---")
        
        # Question input
        question = st.text_input(
            "Enter your question:",
            key="question_input",
            placeholder="What would you like to know about your documents?"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            ask_button = st.button("🔍 Ask", type="primary")
        
        if ask_button and question:
            if st.session_state.qa_chain:
                with st.spinner("🤔 Thinking (this may take 10-30 seconds with local AI)..."):
                    try:
                        response = st.session_state.qa_chain.invoke({"query": question})
                        answer = response["result"]
                        source_documents = response.get("source_documents", [])
                        
                        # Add to chat history
                        st.session_state.chat_history.append((question, answer, source_documents))
                        
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
                        st.error("Make sure Ollama is still running!")
            else:
                st.error("QA chain not initialized. Please process documents first.")
        
        elif ask_button and not question:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()