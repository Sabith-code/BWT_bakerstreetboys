@echo off
echo 🪄 Abra Code Abra - Backend Setup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To start the backend:
echo    1. Activate venv: venv\Scripts\activate
echo    2. Run: python app.py
echo.
echo 📍 Backend will run at: http://localhost:5000
echo.
pause