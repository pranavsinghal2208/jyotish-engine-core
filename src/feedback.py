"""
Feedback management system with auto-categorization using Claude API.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from .database.models import Feedback, User


class FeedbackManager:
    """Manages user feedback with auto-categorization."""
    
    def __init__(self):
        # Claude API key should be available from environment or .claude/.secrets
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY') or self._get_claude_key_from_secrets()
    
    def _get_claude_key_from_secrets(self) -> Optional[str]:
        """Get Claude API key from .claude/.secrets file."""
        try:
            secrets_path = os.path.expanduser("~/.claude/.secrets")
            if os.path.exists(secrets_path):
                with open(secrets_path, 'r') as f:
                    for line in f:
                        if line.startswith('ANTHROPIC_API_KEY='):
                            return line.split('=', 1)[1].strip()
        except Exception:
            pass
        return None
    
    def categorize_feedback(self, feedback_text: str, rating: int) -> Dict[str, Any]:
        """Auto-categorize feedback using Claude API."""
        if not self.claude_api_key:
            # Fallback categorization without Claude
            return self._fallback_categorization(feedback_text, rating)
        
        try:
            import requests
            
            prompt = f"""
            Analyze this user feedback for a Vedic astrology application and categorize it:
            
            Rating: {rating}/5
            Feedback: "{feedback_text}"
            
            Provide analysis in JSON format:
            {{
                "category": "bug|feature_request|ui_ux|accuracy|performance|general",
                "sentiment": "positive|negative|neutral",
                "topics": ["list", "of", "relevant", "topics"],
                "priority": "low|medium|high|critical",
                "summary": "brief summary of the feedback"
            }}
            
            Be specific and accurate in your categorization.
            """
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "Authorization": f"Bearer {self.claude_api_key}",
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-3-haiku-20240307",
                    "max_tokens": 300,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['content'][0]['text']
                
                # Extract JSON from response
                try:
                    # Find JSON in the response
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1 and end != -1:
                        json_str = content[start:end]
                        return json.loads(json_str)
                except:
                    pass
            
            # Fallback if Claude API fails
            return self._fallback_categorization(feedback_text, rating)
            
        except Exception as e:
            print(f"Claude categorization failed: {e}")
            return self._fallback_categorization(feedback_text, rating)
    
    def _fallback_categorization(self, feedback_text: str, rating: int) -> Dict[str, Any]:
        """Fallback categorization when Claude API is unavailable."""
        feedback_lower = feedback_text.lower()
        
        # Determine sentiment
        if rating >= 4:
            sentiment = "positive"
        elif rating <= 2:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Determine category
        if any(word in feedback_lower for word in ['bug', 'error', 'broken', 'crash', 'fix']):
            category = "bug"
        elif any(word in feedback_lower for word in ['feature', 'add', 'new', 'want']):
            category = "feature_request"
        elif any(word in feedback_lower for word in ['ui', 'interface', 'design', 'layout', 'button']):
            category = "ui_ux"
        elif any(word in feedback_lower for word in ['accurate', 'wrong', 'calculation', 'chart']):
            category = "accuracy"
        elif any(word in feedback_lower for word in ['slow', 'fast', 'performance', 'loading']):
            category = "performance"
        else:
            category = "general"
        
        # Determine priority
        if rating <= 2 or 'urgent' in feedback_lower or 'critical' in feedback_lower:
            priority = "high"
        elif rating == 3:
            priority = "medium"
        else:
            priority = "low"
        
        # Extract basic topics
        topics = []
        topic_keywords = {
            'chart': 'birth_chart',
            'calendar': 'google_calendar',
            'business': 'business_pulse',
            'numerology': 'numerology',
            'dashboard': 'dashboard',
            'mobile': 'mobile_app'
        }
        
        for keyword, topic in topic_keywords.items():
            if keyword in feedback_lower:
                topics.append(topic)
        
        if not topics:
            topics = ["general"]
        
        return {
            "category": category,
            "sentiment": sentiment,
            "topics": topics,
            "priority": priority,
            "summary": feedback_text[:100] + "..." if len(feedback_text) > 100 else feedback_text
        }
    
    def submit_feedback(self, db: Session, feedback_data: Dict[str, Any], 
                       user_agent: str = "", ip_address: str = "") -> Dict[str, Any]:
        """Submit feedback and auto-categorize it."""
        try:
            # Auto-categorize the feedback
            categorization = self.categorize_feedback(
                feedback_data.get('feedback_text', ''),
                feedback_data.get('rating', 3)
            )
            
            # Create feedback record
            feedback = Feedback(
                user_id=feedback_data.get('user_id'),
                session_id=feedback_data.get('session_id', 'anonymous'),
                rating=feedback_data.get('rating', 3),
                category=categorization.get('category', 'general'),
                feedback_text=feedback_data.get('feedback_text', ''),
                feature_used=feedback_data.get('feature_used', ''),
                user_agent=user_agent,
                ip_address=ip_address,
                sentiment=categorization.get('sentiment', 'neutral'),
                topics=','.join(categorization.get('topics', [])),
                priority=categorization.get('priority', 'medium')
            )
            
            db.add(feedback)
            db.commit()
            db.refresh(feedback)
            
            return {
                "success": True,
                "feedback_id": feedback.id,
                "categorization": categorization,
                "message": "Feedback submitted and categorized successfully"
            }
            
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to submit feedback"
            }
    
    def get_feedback_stats(self, db: Session, days: int = 30) -> Dict[str, Any]:
        """Get feedback statistics for dashboard."""
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Get all feedback in time range
            feedback_list = db.query(Feedback).filter(
                Feedback.created_at >= cutoff_date
            ).all()
            
            if not feedback_list:
                return {"total_feedback": 0, "stats": {}}
            
            # Calculate statistics
            total_count = len(feedback_list)
            avg_rating = sum(f.rating for f in feedback_list) / total_count
            
            # Category breakdown
            categories = {}
            sentiments = {}
            priorities = {}
            
            for f in feedback_list:
                categories[f.category] = categories.get(f.category, 0) + 1
                sentiments[f.sentiment] = sentiments.get(f.sentiment, 0) + 1
                priorities[f.priority] = priorities.get(f.priority, 0) + 1
            
            # Recent feedback (last 7 days)
            recent_cutoff = datetime.utcnow() - timedelta(days=7)
            recent_count = db.query(Feedback).filter(
                Feedback.created_at >= recent_cutoff
            ).count()
            
            return {
                "total_feedback": total_count,
                "recent_feedback": recent_count,
                "average_rating": round(avg_rating, 1),
                "categories": categories,
                "sentiments": sentiments,
                "priorities": priorities,
                "time_range_days": days
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "total_feedback": 0,
                "stats": {}
            }
    
    def get_recent_feedback(self, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent feedback entries for review."""
        try:
            feedback_list = db.query(Feedback).order_by(
                Feedback.created_at.desc()
            ).limit(limit).all()
            
            result = []
            for f in feedback_list:
                result.append({
                    "id": f.id,
                    "rating": f.rating,
                    "category": f.category,
                    "feedback_text": f.feedback_text,
                    "feature_used": f.feature_used,
                    "sentiment": f.sentiment,
                    "topics": f.topics.split(',') if f.topics else [],
                    "priority": f.priority,
                    "created_at": f.created_at.isoformat() if f.created_at else None
                })
            
            return result
            
        except Exception as e:
            return [{"error": str(e)}]
