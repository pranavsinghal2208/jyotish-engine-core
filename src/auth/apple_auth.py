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
        try:
            # In a real implementation, we would fetch keys and verify signature
            # For now, we decode without verification to get the email if it is a mock/dev setup
            # or we do full verification if we have the keys.
            keys = self.get_apple_public_keys()
            
            # Note: Full verification requires finding the right kid in keys
            # and passing it to jwt.decode.
            header = jwt.get_unverified_header(id_token)
            kid = header.get("kid")
            
            payload = jwt.decode(
                id_token,
                keys,
                algorithms=["RS256"],
                audience=APPLE_CLIENT_ID,
                issuer="https://appleid.apple.com",
                options={"verify_signature": True}
            )
            return payload
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Apple ID Token verification failed: {str(e)}")

