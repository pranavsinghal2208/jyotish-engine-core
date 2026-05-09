// Analytics Tracking for Jyotish Engine Core

class AnalyticsTracker {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.pageViews = new Set();
        this.lastActivity = Date.now();
        
        // Track initial page load
        this.trackPageView(window.location.pathname);
        
        // Track user activity
        this.setupActivityTracking();
        
        // Track beforeunload for session duration
        window.addEventListener('beforeunload', () => {
            this.trackSessionDuration();
        });
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    async trackEvent(eventType, eventData = {}) {
        try {
            const payload = {
                event_type: eventType,
                session_id: this.sessionId,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                ...eventData
            };
            
            const response = await fetch('/api/analytics/track', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                console.warn('Analytics tracking failed:', response.status);
            }
        } catch (error) {
            console.warn('Analytics tracking error:', error);
        }
    }
    
    trackPageView(page = window.location.pathname) {
        // Avoid duplicate page view tracking
        if (this.pageViews.has(page)) return;
        this.pageViews.add(page);
        
        this.trackEvent('page_view', {
            page: page,
            referrer: document.referrer,
            screen_resolution: `${window.screen.width}x${window.screen.height}`,
            viewport_size: `${window.innerWidth}x${window.innerHeight}`
        });
    }
    
    trackFeatureUsage(feature, metadata = {}) {
        this.trackEvent('feature_usage', {
            feature: feature,
            metadata: metadata
        });
        
        // Update last activity
        this.lastActivity = Date.now();
    }
    
    trackConversion(conversionType, value = 0, metadata = {}) {
        this.trackEvent('conversion', {
            conversion_type: conversionType,
            value: value,
            metadata: metadata
        });
    }
    
    setupActivityTracking() {
        // Track clicks on key elements
        document.addEventListener('click', (e) => {
            const target = e.target.closest('[data-track]');
            if (target) {
                const feature = target.dataset.track;
                this.trackFeatureUsage(feature, {
                    element: target.tagName.toLowerCase(),
                    text: target.textContent?.trim().substring(0, 50)
                });
            }
        });
        
        // Track form submissions
        document.addEventListener('submit', (e) => {
            const form = e.target;
            if (form.id) {
                this.trackFeatureUsage('form_submission', {
                    form_id: form.id,
                    form_action: form.action
                });
            }
        });
        
        // Track time spent on page
        setInterval(() => {
            if (Date.now() - this.lastActivity > 30000) { // 30 seconds of inactivity
                this.trackFeatureUsage('page_engagement', {
                    time_spent: Math.floor((Date.now() - this.lastActivity) / 1000)
                });
            }
        }, 30000);
    }
    
    trackSessionDuration() {
        const duration = Math.floor((Date.now() - parseInt(this.sessionId.split('_')[1])) / 1000);
        this.trackFeatureUsage('session_end', {
            duration_seconds: duration,
            pages_viewed: this.pageViews.size
        });
    }
}

// Track chart generation
function trackChartGeneration(birthData) {
    if (window.analyticsTracker) {
        window.analyticsTracker.trackFeatureUsage('chart_generation', {
            has_name: !!birthData.full_name,
            has_location: !!birthData.location_name,
            timezone_offset: birthData.timezone_offset
        });
    }
}

// Track numerology calculation
function trackNumerologyCalculation(birthDate, name) {
    if (window.analyticsTracker) {
        window.analyticsTracker.trackFeatureUsage('numerology_calculation', {
            has_birth_date: !!birthDate,
            name_length: name ? name.length : 0
        });
    }
}

// Track feedback submission
function trackFeedbackSubmission(rating, featureUsed) {
    if (window.analyticsTracker) {
        window.analyticsTracker.trackConversion('feedback_submission', rating, {
            rating: rating,
            feature_used: featureUsed
        });
    }
}

// Initialize analytics when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    window.analyticsTracker = new AnalyticsTracker();
    
    // Add tracking attributes to key elements
    const trackableElements = [
        { selector: '#generateBtn', feature: 'chart_generation_click' },
        { selector: '[data-track="numerology"]', feature: 'numerology_click' },
        { selector: '.feedback-toggle', feature: 'feedback_widget_open' }
    ];
    
    trackableElements.forEach(({ selector, feature }) => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => el.setAttribute('data-track', feature));
    });
});
