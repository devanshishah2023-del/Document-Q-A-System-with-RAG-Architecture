#!/bin/bash

echo "🚀 Starting Document Q&A with RAG..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first:"
    echo "    bash setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" &> /dev/null; then
    echo "❌ Dependencies not installed!"
    echo "Please run setup.sh first:"
    echo "    bash setup.sh"
    exit 1
fi

# Run the app
echo "✅ Starting Streamlit app..."
echo ""
echo "🌐 Opening http://localhost:8501 in your browser..."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
