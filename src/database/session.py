import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .models import Base

load_dotenv()

# Default to SQLite for local development if POSTGRES_URL is not provided
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cosmic_os.db")

# For SQLite, we need connect_args={"check_same_thread": False}
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
