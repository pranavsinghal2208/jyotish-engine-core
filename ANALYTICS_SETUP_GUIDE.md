# Analytics Setup Guide for Jyotish Engine Core

## 🎯 **How to Track Website Visitors and Usage**

This guide shows you how to implement comprehensive analytics tracking for your Vedic Astrology application.

---

## 📊 **Available Analytics Solutions**

### **1. Built-in Analytics (FREE - Ready to Use)**
- ✅ **Page views** - Tracks visits to different pages
- ✅ **Feature usage** - Monitors chart generation, numerology, feedback
- ✅ **User engagement** - Session duration, bounce rate
- ✅ **Conversions** - Feedback submissions, user registrations
- ✅ **Privacy-compliant** - Anonymized IP addresses

### **2. Google Analytics 4 (Optional - Enhanced Tracking)**
- 📈 **Advanced metrics** - Demographics, traffic sources, conversion funnels
- 🌍 **Global insights** - Geographic data, device types
- 📱 **Real-time monitoring** - Live user activity
- 🔗 **Integration** - Connects with other Google tools

---

## 🚀 **Quick Start - Built-in Analytics**

### **Step 1: Add Analytics to Your App**
Already implemented! The analytics system is built into your Jyotish Engine Core.

### **Step 2: Include Analytics Scripts**
Add these lines to your `src/static/index.html` before `</body>`:

```html
<!-- Analytics Tracking -->
<script src="analytics.js"></script>
```

### **Step 3: Test Analytics**
1. Start your server: `python -m src.main`
2. Visit `http://127.0.0.1:8000`
3. Open browser Developer Tools → Network tab
4. Look for `/api/analytics/track` requests

### **Step 4: View Analytics Dashboard**
Create an admin page or add to existing dashboard:
```html
<!-- Add to any admin/dashboard page -->
<link rel="stylesheet" href="analytics-dashboard.css">
<script src="analytics-dashboard.js"></script>

<!-- Include the dashboard HTML -->
<!-- Copy content from analytics_dashboard.html -->
```

---

## 📈 **What Gets Tracked Automatically**

| Event Type | What It Tracks | Example |
|------------|----------------|---------|
| **Page Views** | URL visits | `/` (homepage), `/api/chart` (API calls) |
| **Feature Usage** | User actions | Chart generation, numerology calculation |
| **Conversions** | Key actions | Feedback submission, user registration |
| **Engagement** | User behavior | Time on page, click patterns |

---

## 🔧 **Optional: Google Analytics 4 Setup**

### **Step 1: Create GA4 Property**
1. Go to [Google Analytics](https://analytics.google.com/)
2. Create a new GA4 property
3. Get your **Measurement ID** (format: `G-XXXXXXXXXX`)

### **Step 2: Set Environment Variables**
```bash
# Add to your shell profile (~/.zshrc)
export GA_MEASUREMENT_ID="G-XXXXXXXXXX"
export GA_API_SECRET="your-api-secret"
```

### **Step 3: Restart Server**
```bash
# Restart your FastAPI server to pick up new environment variables
python -m src.main
```

### **Step 4: Verify GA Integration**
Check your GA4 real-time dashboard - you should see events flowing in!

---

## 📊 **API Endpoints for Analytics**

### **Track Events**
```bash
POST /api/analytics/track
Content-Type: application/json

{
  "event_type": "page_view|feature_usage|conversion",
  "session_id": "session_123",
  "page": "/",
  "feature": "chart_generation",
  "conversion_type": "feedback_submission",
  "value": 5,
  "metadata": {"custom": "data"}
}
```

### **View Analytics Summary**
```bash
GET /api/analytics/summary?days=30

# Returns:
{
  "total_visitors": 150,
  "total_page_views": 450,
  "unique_users": 120,
  "registered_users": 25,
  "feedback_submissions": 18,
  "avg_rating": 4.2,
  "feature_usage": {
    "chart_generation": 89,
    "numerology_calculation": 34,
    "feedback_submission": 18
  }
}
```

---

## 🎯 **Key Metrics to Monitor**

### **Traffic Metrics**
- **Total Visitors**: How many people visit your site
- **Page Views**: How many pages they view
- **Unique Users**: How many distinct people
- **Session Duration**: How long they stay

### **Engagement Metrics**
- **Chart Generations**: Core feature usage
- **Numerology Calculations**: New feature adoption
- **Feedback Submissions**: User satisfaction indicator
- **Conversion Rate**: Visitors who take action

### **Quality Metrics**
- **Average Rating**: From feedback widget
- **Bounce Rate**: Visitors who leave quickly
- **Feature Usage Distribution**: Which features are popular

---

## 🔍 **How to View Analytics Data**

### **Method 1: Built-in Dashboard (Recommended)**
1. Create `/analytics` route in your FastAPI app
2. Add the dashboard HTML component
3. View real-time metrics at `http://127.0.0.1:8000/analytics`

### **Method 2: API Queries**
Use curl or browser to query analytics:
```bash
curl http://127.0.0.1:8000/api/analytics/summary
```

### **Method 3: Database Queries**
Direct database access for detailed analysis:
```sql
-- View recent page views
SELECT * FROM analytics_events 
WHERE event_type = 'page_view' 
ORDER BY timestamp DESC LIMIT 10;

-- Count feature usage
SELECT feature, COUNT(*) as usage_count
FROM analytics_events 
WHERE event_type = 'feature_usage'
GROUP BY feature
ORDER BY usage_count DESC;
```

---

## 📱 **Frontend Integration Examples**

### **Track Page Views**
```javascript
// Automatically tracked when analytics.js loads
// Manual tracking for SPAs:
analyticsTracker.trackPageView('/numerology');
```

### **Track Feature Usage**
```javascript
// When user generates a chart
analyticsTracker.trackFeatureUsage('chart_generation', {
    has_name: true,
    has_location: true
});

// When user calculates numerology
analyticsTracker.trackFeatureUsage('numerology_calculation', {
    has_birth_date: true,
    name_length: 12
});
```

### **Track Conversions**
```javascript
// When user submits feedback
analyticsTracker.trackConversion('feedback_submission', 5, {
    rating: 5,
    feature_used: 'dashboard'
});
```

---

## 🔐 **Privacy & Compliance**

### **GDPR/CCPA Compliant**
- ✅ **IP Anonymization** - Last octet removed
- ✅ **No Personal Data** - No emails, names stored
- ✅ **Session-based** - No persistent user tracking
- ✅ **Opt-out Ready** - Easy to disable tracking

### **Data Retention**
- **Local Analytics**: Stored in your database (control retention)
- **Google Analytics**: Google's retention policies apply

---

## 🚀 **Next Steps**

### **Immediate (Today)**
1. ✅ Add analytics scripts to your HTML
2. ✅ Test tracking with browser dev tools
3. ✅ View analytics dashboard

### **Week 1**
1. Set up Google Analytics 4 (optional)
2. Create admin dashboard for metrics
3. Set up automated reports

### **Month 1**
1. Implement A/B testing framework
2. Add conversion funnel tracking
3. Create user cohort analysis

---

## 📞 **Need Help?**

**Test Commands:**
```bash
# Test analytics API
curl -X POST http://127.0.0.1:8000/api/analytics/track \
  -H "Content-Type: application/json" \
  -d '{"event_type": "test", "session_id": "test-session"}'

# View summary
curl http://127.0.0.1:8000/api/analytics/summary
```

**Common Issues:**
- **No events showing**: Check browser console for JavaScript errors
- **GA not working**: Verify `GA_MEASUREMENT_ID` and `GA_API_SECRET`
- **API errors**: Check server logs for analytics endpoint errors

---

## 🎯 **Success Metrics**

**Track these KPIs:**
- **Daily Active Users**: Visitors per day
- **Feature Adoption**: % using numerology/feedback
- **Engagement Score**: Average session duration
- **Conversion Rate**: Feedback submissions per visitor
- **User Satisfaction**: Average feedback rating

**Your analytics system is now ready to provide deep insights into user behavior and feature adoption!** 🚀
