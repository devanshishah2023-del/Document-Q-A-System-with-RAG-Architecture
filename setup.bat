@echo off
echo.
echo ================================================
echo   Document Q&A with RAG - Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Get your OpenAI API key from:
echo    https://platform.openai.com/api-keys
echo.
echo 2. Run the app:
echo    streamlit run app.py
echo.
echo 3. Enter your API key in the sidebar
echo.
echo 4. Upload documents and start asking questions!
echo.
echo For detailed instructions, see README.md
echo.
pause
