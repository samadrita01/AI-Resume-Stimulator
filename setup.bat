@echo off
REM ────────────────────────────────────────────────────────────
REM AI Resume Analyzer - Setup Script for Windows
REM ────────────────────────────────────────────────────────────

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  AI Resume Analyzer - Global Setup Script              ║
echo ║  Platform: Windows                                     ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found. Please install Python 3.8 or higher.
    echo   Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo [2/5] Setting up virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo ✓ Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully
echo.

REM Create directories
echo [5/5] Creating data directories...
if not exist data mkdir data
if not exist uploads mkdir uploads
if not exist logs mkdir logs
echo ✓ Directories created
echo.

echo ╔════════════════════════════════════════════════════════╗
echo ║  ✓ Setup Complete!                                     ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo To run the application:
echo.
echo   1. Activate virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Start the application:
echo      streamlit run ai_resume_analyzer_global.py
echo.
echo   3. Access in browser:
echo      http://localhost:8501
echo.
echo For network access from other machines:
echo      streamlit run ai_resume_analyzer_global.py --server.address=0.0.0.0
echo.
pause
