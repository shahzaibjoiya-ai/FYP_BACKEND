@echo off
REM Setup script for Deepfake Detection Backend (Windows)

echo.
echo ======================================================
echo Deepfake Detection Backend - Setup
echo ======================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python version:
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo.
echo Creating directories...
if not exist models mkdir models
if not exist uploads mkdir uploads
if not exist logs mkdir logs

echo.
echo ======================================================
echo Setup completed successfully!
echo ======================================================
echo.
echo To run the backend:
echo   1. Activate virtual environment: venv\Scripts\activate.bat
echo   2. Run the server: python main.py
echo.
echo The API will be available at http://localhost:5000
echo ======================================================
echo.
pause
