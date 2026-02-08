# 📚 RAG Document Q&A - Free & Open Source

A powerful document question-answering system using Retrieval-Augmented Generation (RAG) with **100% free** local LLMs via Ollama. No API keys required!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🌟 Features

- ✅ **100% Free** - Uses Ollama for local LLM inference
- 📄 **Multiple Document Formats** - PDF, TXT, and DOCX
- 🔍 **Semantic Search** - Vector-based retrieval with ChromaDB
- 💬 **Interactive UI** - Clean Streamlit interface
- 🗄️ **Persistent Storage** - Saves your document embeddings
- 🔒 **Privacy First** - All processing happens locally

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai) installed

### Installation

1. **Install Ollama and pull a model**:
```bash
# Download from ollama.ai, then:
ollama pull llama2
```

2. **Clone and setup**:
```bash
git clone https://github.com/devanshishah2023-del/Document-Q-A-System-with-RAG-Architecture.git
cd Document-Q-A-System-with-RAG-Architecture

# Setup (macOS/Linux)
chmod +x setup.sh
./setup.sh

# Or manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Run the app**:
```bash
streamlit run app_free.py
```

Open http://localhost:8501 in your browser

## 📖 Usage

1. Upload documents (PDF, TXT, or DOCX)
2. Click "Process Documents" to create embeddings
3. Ask questions about your documents
4. Get AI-powered answers!

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Ollama (llama2/mistral/etc.)
- **Vector DB**: ChromaDB
- **Framework**: LangChain

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Free local LLMs
- [LangChain](https://langchain.com) - RAG framework
- [Streamlit](https://streamlit.io) - UI framework
- [ChromaDB](https://www.trychroma.com/) - Vector storage

---

⭐ Star this repo if you find it useful!
