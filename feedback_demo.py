#!/usr/bin/env python3
"""
Feedback Demo for Jyotish Engine Core
Test the feedback system with auto-categorization.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from feedback import FeedbackManager

def main():
    print("💬 Jyotish Engine Core - Feedback Demo")
    print("=" * 50)
    
    manager = FeedbackManager()
    
    # Sample feedback data
    sample_feedback = [
        {
            "rating": 5,
            "feedback_text": "Amazing accuracy! The birth chart predictions were spot on.",
            "feature_used": "birth_chart"
        },
        {
            "rating": 3,
            "feedback_text": "The UI is a bit confusing, could use better navigation.",
            "feature_used": "dashboard"
        },
        {
            "rating": 4,
            "feedback_text": "Love the business pulse feature! Would like more detailed insights.",
            "feature_used": "business_pulse"
        },
        {
            "rating": 2,
            "feedback_text": "App crashed when trying to connect Google Calendar.",
            "feature_used": "google_calendar"
        },
        {
            "rating": 5,
            "feedback_text": "The cosmic schedule feature is brilliant!",
            "feature_used": "cosmic_schedule"
        }
    ]
    
    print("🔍 Testing Auto-Categorization (without Claude API - using fallback):")
    print()
    
    for i, feedback in enumerate(sample_feedback, 1):
        print(f"📝 Feedback #{i}:")
        print(f"   Rating: {feedback['rating']}/5")
        print(f"   Text: \"{feedback['feedback_text']}\"")
        print(f"   Feature: {feedback['feature_used']}")
        
        # Test categorization
        categorization = manager.categorize_feedback(
            feedback['feedback_text'], 
            feedback['rating']
        )
        
        print(f"   → Category: {categorization['category']}")
        print(f"   → Sentiment: {categorization['sentiment']}")
        print(f"   → Priority: {categorization['priority']}")
        print(f"   → Topics: {', '.join(categorization['topics'])}")
        print()
    
    print("✅ Feedback categorization demo complete!")
    print("\nTo integrate this into the web app:")
    print("1. The API endpoints /api/feedback are ready")
    print("2. Add feedback widget UI components")
    print("3. Use /api/feedback/stats for dashboard metrics")
    print("4. Use /api/feedback/recent for admin review")
    print("\nNote: For production, set ANTHROPIC_API_KEY for better categorization")

if __name__ == "__main__":
    main()
