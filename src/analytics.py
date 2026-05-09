"""
Analytics tracking for Jyotish Engine Core.
Tracks page views, feature usage, and user engagement.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from .database.models import User


class AnalyticsTracker:
    """Tracks user engagement and feature usage."""
    
    def __init__(self):
        self.ga_measurement_id = os.getenv('GA_MEASUREMENT_ID', '')
        self.ga_api_secret = os.getenv('GA_API_SECRET', '')
    
    def track_page_view(self, page: str, user_agent: str = "", ip_address: str = "", 
                       session_id: str = "", referrer: str = "") -> Dict[str, Any]:
        """Track page view with basic analytics."""
        event_data = {
            "event_type": "page_view",
            "page": page,
            "timestamp": datetime.utcnow().isoformat(),
            "user_agent": user_agent,
            "ip_address": self._anonymize_ip(ip_address),
            "session_id": session_id,
            "referrer": referrer,
            "user_id": None  # Will be set if user is logged in
        }
        
        # Send to Google Analytics if configured
        if self.ga_measurement_id and self.ga_api_secret:
            self._send_to_google_analytics(event_data)
        
        return event_data
    
    def track_feature_usage(self, feature: str, user_id: Optional[int] = None, 
                           session_id: str = "", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Track feature usage (chart generation, numerology, etc.)."""
        event_data = {
            "event_type": "feature_usage",
            "feature": feature,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "session_id": session_id,
            "metadata": metadata or {}
        }
        
        # Send to Google Analytics
        if self.ga_measurement_id and self.ga_api_secret:
            self._send_feature_to_ga(feature, metadata)
        
        return event_data
    
    def track_conversion(self, conversion_type: str, value: float = 0, 
                        user_id: Optional[int] = None, session_id: str = "") -> Dict[str, Any]:
        """Track conversions (feedback submissions, etc.)."""
        event_data = {
            "event_type": "conversion",
            "conversion_type": conversion_type,
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "session_id": session_id
        }
        
        # Send conversion to Google Analytics
        if self.ga_measurement_id and self.ga_api_secret:
            self._send_conversion_to_ga(conversion_type, value)
        
        return event_data
    
    def _anonymize_ip(self, ip: str) -> str:
        """Anonymize IP address for privacy compliance."""
        if not ip or ip == "127.0.0.1" or ip.startswith("192.168.") or ip.startswith("10."):
            return "local"
        
        parts = ip.split(".")
        if len(parts) == 4:
            # Anonymize last octet
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0"
        return ip
    
    def _send_to_google_analytics(self, event_data: Dict[str, Any]):
        """Send event to Google Analytics 4."""
        try:
            import requests
            
            url = f"https://www.google-analytics.com/mp/collect?measurement_id={self.ga_measurement_id}&api_secret={self.ga_api_secret}"
            
            payload = {
                "client_id": event_data.get("session_id", "anonymous"),
                "events": [{
                    "name": event_data["event_type"],
                    "params": {
                        "page_title": event_data.get("page", ""),
                        "page_location": f"http://localhost:8000{event_data.get('page', '')}",
                        "user_agent": event_data.get("user_agent", ""),
                        "engagement_time_msec": 1000
                    }
                }]
            }
            
            requests.post(url, json=payload, timeout=5)
            
        except Exception as e:
            print(f"GA tracking failed: {e}")
    
    def _send_feature_to_ga(self, feature: str, metadata: Dict[str, Any] = None):
        """Send feature usage to Google Analytics."""
        try:
            import requests
            
            url = f"https://www.google-analytics.com/mp/collect?measurement_id={self.ga_measurement_id}&api_secret={self.ga_api_secret}"
            
            params = {
                "feature_name": feature,
                "engagement_time_msec": 1000
            }
            
            if metadata:
                # Add up to 25 custom parameters
                for key, value in list(metadata.items())[:25]:
                    if isinstance(value, (str, int, float, bool)):
                        params[f"custom_{key}"] = str(value)[:100]  # GA limits
            
            payload = {
                "client_id": "feature_usage",
                "events": [{
                    "name": "feature_used",
                    "params": params
                }]
            }
            
            requests.post(url, json=payload, timeout=5)
            
        except Exception as e:
            print(f"GA feature tracking failed: {e}")
    
    def _send_conversion_to_ga(self, conversion_type: str, value: float):
        """Send conversion event to Google Analytics."""
        try:
            import requests
            
            url = f"https://www.google-analytics.com/mp/collect?measurement_id={self.ga_measurement_id}&api_secret={self.ga_api_secret}"
            
            payload = {
                "client_id": "conversion",
                "events": [{
                    "name": "conversion",
                    "params": {
                        "conversion_type": conversion_type,
                        "value": value,
                        "currency": "USD"
                    }
                }]
            }
            
            requests.post(url, json=payload, timeout=5)
            
        except Exception as e:
            print(f"GA conversion tracking failed: {e}")


class AnalyticsDashboard:
    """Dashboard for viewing analytics data."""
    
    def __init__(self):
        self.tracker = AnalyticsTracker()
    
    def get_analytics_summary(self, db: Session, days: int = 30) -> Dict[str, Any]:
        """Get basic analytics summary (would need database tables for full tracking)."""
        try:
            # For now, return mock data since we don't have analytics tables yet
            # In production, this would query analytics events from database
            
            mock_data = {
                "period": f"Last {days} days",
                "total_visitors": 0,  # Would count unique sessions
                "total_page_views": 0,  # Would count page_view events
                "unique_users": 0,  # Would count distinct user_ids
                "feature_usage": {
                    "chart_generation": 0,
                    "numerology_calculation": 0,
                    "feedback_submission": 0
                },
                "top_pages": [],
                "conversion_rate": 0.0,
                "avg_session_duration": 0,
                "bounce_rate": 0.0
            }
            
            # Get real user count
            user_count = db.query(User).count()
            mock_data["registered_users"] = user_count
            
            # Get feedback stats (we have this endpoint)
            try:
                from .feedback import FeedbackManager
                feedback_manager = FeedbackManager()
                feedback_stats = feedback_manager.get_feedback_stats(db, days)
                if "total_feedback" in feedback_stats:
                    mock_data["feedback_submissions"] = feedback_stats["total_feedback"]
                    mock_data["avg_rating"] = feedback_stats.get("average_rating", 0)
            except:
                mock_data["feedback_submissions"] = 0
            
            return mock_data
            
        except Exception as e:
            return {"error": str(e)}
