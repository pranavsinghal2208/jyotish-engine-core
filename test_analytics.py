#!/usr/bin/env python3
"""
Test Analytics Functionality
Run this to verify analytics tracking is working.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analytics import AnalyticsTracker
import time

def test_analytics():
    print("🧪 Testing Jyotish Engine Core Analytics")
    print("=" * 50)
    
    tracker = AnalyticsTracker()
    
    print("✅ Analytics tracker initialized")
    
    # Test page view tracking
    print("\n📄 Testing page view tracking...")
    result = tracker.track_page_view("/test-page", "TestAgent/1.0", "127.0.0.1", "test-session")
    print(f"✅ Page view tracked: {result['event_type']}")
    
    # Test feature usage tracking
    print("\n🚀 Testing feature usage tracking...")
    result = tracker.track_feature_usage("chart_generation", 1, "test-session", {"test": True})
    print(f"✅ Feature usage tracked: {result['feature']}")
    
    # Test conversion tracking
    print("\n💰 Testing conversion tracking...")
    result = tracker.track_conversion("feedback_submission", 5.0, 1, "test-session")
    print(f"✅ Conversion tracked: {result['conversion_type']}")
    
    # Test IP anonymization
    print("\n🔒 Testing IP anonymization...")
    test_ips = ["192.168.1.100", "10.0.0.1", "203.0.113.195", "127.0.0.1"]
    for ip in test_ips:
        anonymized = tracker._anonymize_ip(ip)
        print(f"   {ip} → {anonymized}")
    
    # Check GA configuration
    print("\n📊 Google Analytics Status:")
    if tracker.ga_measurement_id:
        print(f"   ✅ GA Measurement ID: {tracker.ga_measurement_id[:10]}...")
        print("   ✅ Google Analytics integration ready"    else:
        print("   ⚠️  Google Analytics not configured (optional)")
        print("      Set GA_MEASUREMENT_ID and GA_API_SECRET environment variables")
    
    print("\n🎯 Analytics test completed successfully!")
    print("\nNext steps:")
    print("1. Start your server: python -m src.main")
    print("2. Visit http://127.0.0.1:8000")
    print("3. Check browser Network tab for /api/analytics/track requests")
    print("4. View analytics at: http://127.0.0.1:8000/api/analytics/summary")

if __name__ == "__main__":
    test_analytics()
