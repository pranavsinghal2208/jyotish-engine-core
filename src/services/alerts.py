import json
from ..core.context import CosmicContext
from .lucky_windows import get_lucky_windows

def get_subscription_status(context):
    """Checks user subscription and active alerts."""
    user = context.user
    prefs = json.loads(user.preferences or "{}")
    
    # Foundational Logic: Automate the "Next Peak Window" discovery
    lucky = get_lucky_windows(context)
    next_peak = None
    if lucky and lucky["windows"]:
        next_peak = next((w for w in lucky["windows"] if w["score"] > 70), None)
        
    return {
        "is_subscriber": user.is_subscriber == 1,
        "next_peak_window": next_peak,
        "alert_count": len(prefs.get("active_watches", [])),
        "daily_brief_enabled": prefs.get("daily_brief", True)
    }

def subscribe_to_window(context, window_timestamp):
    """Adds a specific time window to the users personal watch list."""
    user = context.user
    prefs = json.loads(user.preferences or "{}")
    watches = prefs.get("active_watches", [])
    
    if window_timestamp not in watches:
        watches.append(window_timestamp)
        prefs["active_watches"] = watches
        user.preferences = json.dumps(prefs)
        # In a real app, db.commit() would happen in the router
        return {"status": "success", "message": f"Alert set for {window_timestamp}"}
    return {"status": "exists"}