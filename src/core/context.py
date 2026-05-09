from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from ..engine import JyotishEngine
from ..numerology import NumerologyEngine

engine = JyotishEngine()
num_engine = NumerologyEngine()

class CosmicContext:
    """Unified interface for accessing user data + astronomical state."""
    def __init__(self, user):
        self.user = user
        self.is_guest = user.email == "default@psbc.com"
        
    def get_birth_jd(self):
        if not self.user.birth_date: return None
        local_dt = datetime.strptime(f"{self.user.birth_date} {self.user.birth_time}", "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=self.user.tz_offset or 5.5)
        return engine.get_julian_day(utc_dt)

    def get_current_jd(self):
        return engine.get_julian_day(datetime.utcnow())

    def get_state(self):
        """Standard data payload for capabilities."""
        if not self.user.birth_date: return None
        jd_birth = self.get_birth_jd()
        planets_birth = engine.get_planetary_positions(jd_birth)
        
        return {
            "user": self.user,
            "jd_birth": jd_birth,
            "planets_birth": planets_birth,
            "jd_now": self.get_current_jd()
        }