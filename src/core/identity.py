import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..database.models import User

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "psbc-premium-standard-secret-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30
FALLBACK_EMAIL = "default@psbc.com"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_identity(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        # Check legacy cookie for backward compatibility during migration
        legacy_email = request.cookies.get("user_email")
        if legacy_email:
            user = db.query(User).filter(User.email == legacy_email).first()
            if user: return user
        
        # Fallback to Guest
        guest = db.query(User).filter(User.email == FALLBACK_EMAIL).first()
        if not guest:
            guest = User(email=FALLBACK_EMAIL)
            db.add(guest)
            db.commit()
            db.refresh(guest)
        return guest

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")