@echo off
echo.
echo Starting Document Q&A with RAG...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Dependencies not installed!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Run the app
echo [OK] Starting Streamlit app...
echo.
echo Opening http://localhost:8501 in your browser...
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py
