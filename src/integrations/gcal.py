from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timezone

class GoogleCalendarManager:
    def __init__(self, credentials_dict):
        self.creds = Credentials.from_authorized_user_info(credentials_dict)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_upcoming_events(self, max_results=10):
        """Fetches the next N events from the user's primary calendar."""
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=max_results, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])

    def analyze_event_priority(self, event):
        """Simple heuristic to determine if an event is high-stakes."""
        summary = event.get('summary', '').lower()
        description = event.get('description', '').lower()
        
        high_stakes_keywords = ['negotiation', 'contract', 'interview', 'pitch', 'launch', 'review', 'board', 'investor']
        is_high_stakes = any(kw in summary or kw in description for kw in high_stakes_keywords)
        
        return {
            "summary": event.get('summary'),
            "start": event['start'].get('dateTime', event['start'].get('date')),
            "is_high_stakes": is_high_stakes
        }
