import streamlit as st
import streamlit.web.cli as stcli
import sys
import os

# Make app folder accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# We can import directly from app
from app.app import *

# Allow this file to be run directly with 'python app/main.py'
if __name__ == "__main__":
    # Use Streamlit CLI to run the app
    sys.argv = ["streamlit", "run", __file__, "--global.developmentMode=false"]
    sys.exit(stcli.main()) 