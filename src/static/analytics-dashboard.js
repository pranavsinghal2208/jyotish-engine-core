// Analytics Dashboard JavaScript

async function loadAnalyticsData() {
    const periodSelect = document.getElementById('analyticsPeriod');
    const days = periodSelect ? parseInt(periodSelect.value) : 30;
    
    try {
        const response = await fetch(`/api/analytics/summary?days=${days}`);
        const data = await response.json();
        
        if (data.error) {
            console.error('Analytics error:', data.error);
            return;
        }
        
        updateAnalyticsDisplay(data);
        
    } catch (error) {
        console.error('Failed to load analytics:', error);
    }
}

function updateAnalyticsDisplay(data) {
    // Update key metrics
    document.getElementById('totalVisitors').textContent = data.total_visitors || '--';
    document.getElementById('pageViews').textContent = data.total_page_views || '--';
    document.getElementById('uniqueUsers').textContent = data.unique_users || '--';
    document.getElementById('avgRating').textContent = data.avg_rating ? data.avg_rating.toFixed(1) : '--';
    
    // Update feature usage
    const featureUsage = data.feature_usage || {};
    document.getElementById('chartGenerations').textContent = featureUsage.chart_generation || '--';
    document.getElementById('numerologyCalcs').textContent = featureUsage.numerology_calculation || '--';
    document.getElementById('feedbackCount').textContent = data.feedback_submissions || '--';
    
    // Update engagement metrics
    document.getElementById('avgSessionDuration').textContent = 
        data.avg_session_duration ? `${data.avg_session_duration}s` : '--';
    document.getElementById('bounceRate').textContent = 
        data.bounce_rate ? `${(data.bounce_rate * 100).toFixed(1)}%` : '--';
    document.getElementById('conversionRate').textContent = 
        data.conversion_rate ? `${(data.conversion_rate * 100).toFixed(1)}%` : '--';
    
    // Update registered users
    if (data.registered_users !== undefined) {
        // Add registered users metric if not already present
        const userCard = document.querySelector('.metric-card:nth-child(3)');
        if (userCard) {
            userCard.innerHTML = `
                <div class="metric-icon">👤</div>
                <div class="metric-content">
                    <div class="metric-value">${data.registered_users}</div>
                    <div class="metric-label">Registered Users</div>
                </div>
            `;
        }
    }
}

async function loadRecentFeedback() {
    try {
        const response = await fetch('/api/feedback/recent?limit=5');
        const feedbackList = await response.json();
        
        const container = document.getElementById('recentFeedback');
        
        if (!Array.isArray(feedbackList) || feedbackList.length === 0) {
            container.innerHTML = '<p class="no-data">No feedback yet</p>';
            return;
        }
        
        const feedbackHtml = feedbackList.map(feedback => `
            <div class="feedback-item">
                <div class="feedback-header">
                    <span class="feedback-rating">${'⭐'.repeat(feedback.rating)}</span>
                    <span class="feedback-category">${feedback.category}</span>
                </div>
                <p class="feedback-text">${feedback.feedback_text}</p>
                <div class="feedback-meta">
                    <span>${feedback.feature_used}</span>
                    <span>${new Date(feedback.created_at).toLocaleDateString()}</span>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = feedbackHtml;
        
    } catch (error) {
        console.error('Failed to load feedback:', error);
        document.getElementById('recentFeedback').innerHTML = '<p class="no-data">Failed to load feedback</p>';
    }
}

function refreshAnalytics() {
    loadAnalyticsData();
    loadRecentFeedback();
}

// Initialize analytics dashboard
document.addEventListener('DOMContentLoaded', () => {
    // Load initial data
    loadAnalyticsData();
    loadRecentFeedback();
    
    // Set up period change handler
    const periodSelect = document.getElementById('analyticsPeriod');
    if (periodSelect) {
        periodSelect.addEventListener('change', refreshAnalytics);
    }
    
    // Auto-refresh every 5 minutes
    setInterval(refreshAnalytics, 5 * 60 * 1000);
});
