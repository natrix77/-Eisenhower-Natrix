@echo off
echo Starting Eisenhower Matrix app...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python first.
    exit /b 1
)

REM Install dependencies if not already installed
echo Checking/installing dependencies...
pip install -r app\requirements.txt

REM Run the app
echo Starting Streamlit server...
streamlit run app\main.py

pause 