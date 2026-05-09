import json
from ..core.context import CosmicContext
from .lucky_windows import get_lucky_windows

def get_subscription_status(context):
    """Checks user subscription and active alerts with Highest-Fit fallback."""
    user = context.user
    prefs = json.loads(user.preferences or "{}")
    
    # 1. Discover the BEST window (Highest-Fit Logic)
    lucky = get_lucky_windows(context)
    best_window = None
    if lucky and lucky["windows"]:
        # Sort by score descending to find the highest
        sorted_windows = sorted(lucky["windows"], key=lambda x: x["score"], reverse=True)
        best_window = sorted_windows[0]
        
        # Labeling for UX
        if best_window["score"] > 70:
            best_window["label"] = "Strategic Peak"
        else:
            best_window["label"] = "Weekly Opportunity"
        
    return {
        "is_subscriber": user.is_subscriber == 1,
        "next_peak_window": best_window, # This is now the Highest-Fit, never None if data exists
        "alert_count": len(prefs.get("active_watches", [])),
        "daily_brief_enabled": prefs.get("daily_brief", True)
    }

def subscribe_to_window(context, window_timestamp):
    user = context.user
    prefs = json.loads(user.preferences or "{}")
    watches = prefs.get("active_watches", [])
    
    if window_timestamp not in watches:
        watches.append(window_timestamp)
        prefs["active_watches"] = watches
        user.preferences = json.dumps(prefs)
        return {"status": "success", "message": f"Alert set for {window_timestamp}"}
    return {"status": "exists"}