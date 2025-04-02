import streamlit as st
import pandas as pd
import os
import json
import sys

# Use absolute imports for Streamlit Cloud compatibility
from app.components.matrix import EisenhowerMatrix
from app.utils.gmail_integration import GmailAPI

# App title and description
st.set_page_config(page_title="Eisenhower Matrix", page_icon="✅", layout="wide")
st.title("Eisenhower Matrix Task Manager")
st.markdown("""
    Organize your tasks using the Eisenhower Matrix method:
    * **Urgent & Important**: Do immediately
    * **Not Urgent & Important**: Schedule
    * **Urgent & Not Important**: Delegate
    * **Not Urgent & Not Important**: Eliminate
""")

# Initialize session state
if 'tasks' not in st.session_state:
    # Load tasks if they exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    data_file = os.path.join(data_dir, 'tasks.json')
    
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            st.session_state.tasks = json.load(f)
    else:
        st.session_state.tasks = {
            'urgent_important': [],
            'not_urgent_important': [],
            'urgent_not_important': [],
            'not_urgent_not_important': []
        }

if 'gmail_connected' not in st.session_state:
    st.session_state.gmail_connected = False

# Gmail integration sidebar
with st.sidebar:
    st.header("Gmail Integration")
    
    gmail_api = GmailAPI()
    
    if not st.session_state.gmail_connected:
        if st.button("Connect to Gmail"):
            auth_url = gmail_api.get_authorization_url()
            st.markdown(f"[Authorize App]({auth_url})")
            st.text_input("Enter authorization code:", key="auth_code")
            
            if st.session_state.auth_code:
                if gmail_api.authenticate_with_code(st.session_state.auth_code):
                    st.session_state.gmail_connected = True
                    st.success("Connected to Gmail!")
                    st.rerun()
                else:
                    st.error("Failed to authenticate. Try again.")
    else:
        st.success("Connected to Gmail!")
        
        # Gmail query options
        st.subheader("Import Emails as Tasks")
        query = st.text_input("Search term (optional)", placeholder="from:someone@example.com")
        max_results = st.slider("Max emails to fetch", 1, 50, 10)
        
        if st.button("Fetch Emails"):
            with st.spinner("Fetching emails..."):
                emails = gmail_api.get_emails(query, max_results)
                
                if emails:
                    # Display emails and let user select which ones to add
                    selected_emails = []
                    for i, email in enumerate(emails):
                        if st.checkbox(f"{email['sender']}: {email['subject']}", key=f"email_{i}"):
                            selected_emails.append(email)
                    
                    if selected_emails and st.button("Add Selected as Tasks"):
                        EisenhowerMatrix.add_emails_as_tasks(selected_emails)
                        st.success(f"Added {len(selected_emails)} emails as tasks!")
                        st.rerun()
                else:
                    st.info("No emails found matching your criteria.")

# Main content - Eisenhower Matrix UI
matrix = EisenhowerMatrix(st.session_state.tasks)
matrix.display()

# Save tasks on changes
if st.button("Save Tasks"):
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    data_file = os.path.join(data_dir, 'tasks.json')
    
    with open(data_file, 'w') as f:
        json.dump(st.session_state.tasks, f)
    st.success("Tasks saved successfully!") 