import json
from datetime import datetime, date
from sqlalchemy import func
from ..database.models import User, Feedback

def get_ecosystem_metrics(db_session):
    """Calculates the 500-user / 30-percent / 90-percent KPIs."""
    total_users = db_session.query(User).count()
    subscribers = db_session.query(User).filter(User.is_subscriber == 1).count()
    
    # Conversion Rate (Target: 30%)
    conversion_rate = (subscribers / total_users * 100) if total_users > 0 else 0
    
    # Target Progress (Target: 500 users)
    acquisition_progress = (total_users / 500 * 100)
    
    # Mock Retention (Calculated via active sessions in last 30 days in real prod)
    retention_rate = 90.0 # Baseline for now
    
    return {
        "acquisition": {
            "current": total_users,
            "target": 500,
            "progress_pct": round(acquisition_progress, 1)
        },
        "monetization": {
            "subscribers": subscribers,
            "rate_pct": round(conversion_rate, 1),
            "target_pct": 30.0
        },
        "health": {
            "retention_pct": retention_rate,
            "target_pct": 90.0
        }
    }

def calculate_unit_economics(metrics):
    """Estimates operational costs per user profile."""
    user_count = metrics["acquisition"]["current"]
    
    # Estimated Costs (Daily)
    claude_cost_per_user = 0.05  # $0.05 for deep insights
    whatsapp_cost_per_msg = 0.01 # $0.01
    
    daily_burn = user_count * (claude_cost_per_user + whatsapp_cost_per_msg)
    
    return {
        "daily_burn_usd": round(daily_burn, 2),
        "monthly_burn_usd": round(daily_burn * 30, 2),
        "break_even_sub_price": round((daily_burn * 30) / (metrics["monetization"]["subscribers"] or 1), 2)
    }