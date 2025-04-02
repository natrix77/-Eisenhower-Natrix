import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import streamlit as st
import json
from datetime import datetime
from pathlib import Path

class GmailAPI:
    # Gmail API setup
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self):
        self.creds = None
        self.service = None
        
        # Set up file paths
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        os.makedirs(data_dir, exist_ok=True)
        self.TOKEN_PATH = os.path.join(data_dir, 'token.pickle')
        self.CREDENTIALS_PATH = os.path.join(data_dir, 'credentials.json')
        
        # Try to use Streamlit secrets if available (for Streamlit Cloud)
        if 'google' in st.secrets:
            try:
                # Create credentials file from secrets
                with open(self.CREDENTIALS_PATH, 'w') as f:
                    json.dump(st.secrets['google'], f)
                st.sidebar.success("Using credentials from Streamlit secrets")
            except Exception as e:
                st.sidebar.error(f"Error loading credentials from secrets: {e}")
        
        # Try to load saved credentials if they exist
        if os.path.exists(self.TOKEN_PATH):
            with open(self.TOKEN_PATH, 'rb') as token:
                try:
                    self.creds = pickle.load(token)
                except Exception:
                    # If token is invalid, proceed without credentials
                    pass
                
        # If credentials are valid, build the service
        if self.creds and self.creds.valid:
            self.service = build('gmail', 'v1', credentials=self.creds)
    
    def get_authorization_url(self):
        """Generate the authorization URL for Gmail API access."""
        # Check if credentials.json exists
        if not os.path.exists(self.CREDENTIALS_PATH):
            # Create a default creds file with instructions
            Path(self.CREDENTIALS_PATH).parent.mkdir(parents=True, exist_ok=True)
            
            creds_instructions = {
                "instructions": "Replace this file with your actual credentials.json from Google Cloud Console",
                "steps": [
                    "1. Go to https://console.cloud.google.com/",
                    "2. Create a new project",
                    "3. Enable the Gmail API",
                    "4. Create an OAuth consent screen (external)",
                    "5. Create OAuth client ID credentials (Desktop application)",
                    "6. Download the credentials.json file",
                    "7. Replace this file with the downloaded credentials.json"
                ]
            }
            
            with open(self.CREDENTIALS_PATH, 'w') as f:
                json.dump(creds_instructions, f, indent=4)
            
            return "#instructions"  # This will be rendered as a link to instructions
            
        flow = InstalledAppFlow.from_client_secrets_file(
            self.CREDENTIALS_PATH, 
            self.SCOPES
        )
        return flow.authorization_url(access_type='offline', include_granted_scopes='true')[0]
    
    def authenticate_with_code(self, code):
        """Complete the OAuth flow with the provided authorization code."""
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.CREDENTIALS_PATH, 
                self.SCOPES
            )
            
            # Exchange the code for credentials
            flow.fetch_token(code=code)
            self.creds = flow.credentials
            
            # Save the credentials for future use
            os.makedirs(os.path.dirname(self.TOKEN_PATH), exist_ok=True)
            with open(self.TOKEN_PATH, 'wb') as token:
                pickle.dump(self.creds, token)
            
            # Build the service
            self.service = build('gmail', 'v1', credentials=self.creds)
            return True
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return False
    
    def get_emails(self, query='', max_results=10):
        """Fetch emails based on the query."""
        if not self.service:
            st.error("Gmail API service not initialized. Please authenticate first.")
            return []
        
        try:
            # Get list of messages that match the query
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                return []
            
            # Fetch full details for each message
            emails = []
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                # Extract email details from message payload
                headers = msg['payload']['headers']
                subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), 'No Subject')
                sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), 'Unknown Sender')
                date = next((header['value'] for header in headers if header['name'].lower() == 'date'), None)
                
                # Get message body snippet
                snippet = msg.get('snippet', '')
                
                # Create email object
                email = {
                    'id': msg['id'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'snippet': snippet
                }
                
                emails.append(email)
            
            return emails
            
        except Exception as e:
            st.error(f"Error fetching emails: {e}")
            return [] 