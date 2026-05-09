from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    location_name = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    birth_date = Column(String) # YYYY-MM-DD
    birth_time = Column(String) # HH:MM
    tz_offset = Column(Float, default=5.5)
    is_subscriber = Column(Integer, default=0) # 0=Free, 1=Premium
    preferences = Column(String, default="{}")
    persona = Column(String, index=True) # e.g. The Kinetic, The Sovereign
    primary_pain_point = Column(String, index=True) # Efficiency, Cash, Cost # JSON string of alert settings
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to credentials
    credentials = relationship("OAuthCredential", back_populates="user", uselist=False)

class OAuthCredential(Base):
    __tablename__ = 'credentials'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(String)
    refresh_token = Column(String)
    token_uri = Column(String)
    client_id = Column(String)
    client_secret = Column(String)
    scopes = Column(String) # Stored as a comma-separated string

    user = relationship("User", back_populates="credentials")

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_id = Column(String, index=True)  # For anonymous feedback
    rating = Column(Integer)  # 1-5 stars
    category = Column(String, index=True)  # Auto-categorized by Claude
    feedback_text = Column(String)
    feature_used = Column(String)  # Which feature they were using
    user_agent = Column(String)
    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Auto-categorized fields
    sentiment = Column(String)  # positive, negative, neutral
    topics = Column(String)  # comma-separated topics
    priority = Column(String)  # low, medium, high, critical
    
    user = relationship("User", back_populates="feedback")

# Add relationship to User model
User.feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")

class NumerologyProfile(Base):
    __tablename__ = 'numerology_profiles'

    id         = Column(Integer, primary_key=True)
    label      = Column(String, unique=True, index=True)   # nickname e.g. "me", "papa"
    gender     = Column(String)
    first_name = Column(String)
    middle_name= Column(String, nullable=True)
    last_name  = Column(String, nullable=True)
    dob        = Column(String)                            # DD-MM-YYYY
    created_at = Column(DateTime, default=datetime.utcnow)
