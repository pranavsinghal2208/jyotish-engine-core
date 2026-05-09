import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from fastapi import Request as FastAPIRequest, HTTPException
from fastapi.responses import RedirectResponse

# Define scopes for Calendar and Gmail
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/gmail.readonly'
]

# Path to client secret JSON (User must provide this)
CLIENT_SECRETS_FILE = "credentials.json"

class GoogleAuthManager:
    def __init__(self):
        self.client_config = None
        if os.path.exists(CLIENT_SECRETS_FILE):
            with open(CLIENT_SECRETS_FILE, 'r') as f:
                self.client_config = json.load(f)

    def get_login_url(self, redirect_uri: str):
        if not self.client_config:
            raise HTTPException(status_code=500, detail="Google API credentials.json missing.")
        
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return authorization_url, state

    def exchange_code(self, code: str, redirect_uri: str):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials
        result = credentials_to_dict(credentials)
        try:
            import requests as _req
            resp = _req.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {credentials.token}"},
                timeout=5,
            )
            result["email"] = resp.json().get("email", "")
        except Exception:
            result["email"] = ""
        return result

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
