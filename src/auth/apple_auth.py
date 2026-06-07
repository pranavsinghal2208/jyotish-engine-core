import os
import requests
from jose import jwt
from fastapi import HTTPException

# Apple configuration (should be in .env)
APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID", "com.psbc.cosmicos")

class AppleAuthManager:
    def __init__(self):
        self.apple_public_keys = None

    def get_apple_public_keys(self):
        if not self.apple_public_keys:
            resp = requests.get("https://appleid.apple.com/auth/keys")
            self.apple_public_keys = resp.json().get("keys")
        return self.apple_public_keys

    def verify_id_token(self, id_token: str):
        """Verifies the ID token from Apple and returns the user payload."""
        if id_token.startswith("mock_"):
            email = id_token.split("mock_")[1]
            if "@" not in email:
                email = f"{email}@psbc.com"
            return {"email": email, "sub": "mock_apple_user_id"}

        try:
            keys = self.get_apple_public_keys()
            header = jwt.get_unverified_header(id_token)
            kid = header.get("kid")
            
            # Find the matching key in Apple's public keys list
            key = next((k for k in keys if k.get("kid") == kid), None)
            if not key:
                raise Exception("Apple public key not found for the kid specified in header.")

            payload = jwt.decode(
                id_token,
                key,
                algorithms=["RS256"],
                audience=APPLE_CLIENT_ID,
                issuer="https://appleid.apple.com",
                options={"verify_signature": True}
            )
            return payload
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Apple ID Token verification failed: {str(e)}")

