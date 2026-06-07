import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.main import app
from src.database.models import Base, User
from src.database.session import get_db

from sqlalchemy.pool import StaticPool

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_calendar_feed_no_birth_details():
    # Call feed without cookies (which falls back to guest with no birth details by default)
    response = client.get("/api/calendar/feed")
    assert response.status_code == 400
    assert "error" in response.json()

def test_calendar_feed_with_birth_details():
    # 1. Create a user with birth details in the testing DB
    db = TestingSessionLocal()
    test_user_email = "test_calendar_user@psbc.com"
    
    user = db.query(User).filter(User.email == test_user_email).first()
    if not user:
        user = User(
            email=test_user_email,
            birth_date="1987-08-22",
            birth_time="09:55",
            tz_offset=5.5
        )
        db.add(user)
        db.commit()
    db.close()
    
    # 2. Request calendar feed with cookie set to our test user
    response = client.get(
        "/api/calendar/feed",
        cookies={"user_email": test_user_email}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/calendar; charset=utf-8"
    
    content = response.text
    assert "BEGIN:VCALENDAR" in content
    assert "END:VCALENDAR" in content
    assert "PRODID:-//PSBC//Cosmic OS//EN" in content
    assert "X-WR-CALNAME:Cosmic OS Intelligence" in content
    
    # Verify it has exactly 14 events
    events_count = content.count("BEGIN:VEVENT")
    assert events_count == 14, f"Expected 14 events in calendar feed, got {events_count}"
    
    # Verify each event has DTSTART, SUMMARY, and DESCRIPTION
    assert "DTSTART;VALUE=DATE:" in content
    assert "SUMMARY:" in content
    assert "DESCRIPTION:" in content
    assert "STRATEGIC CONTEXT:" in content
    assert "OPERATIONAL RIGOR:" in content
