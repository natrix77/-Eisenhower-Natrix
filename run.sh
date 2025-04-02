#!/bin/bash
# Simple script to run the Eisenhower Matrix app

echo "Starting Eisenhower Matrix app..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "pip not found. Please install pip first."
    exit 1
fi

# Install dependencies if not already installed
echo "Checking/installing dependencies..."
pip install -r app/requirements.txt

# Run the app
echo "Starting Streamlit server..."
streamlit run app/main.py 