import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.engine import JyotishEngine
from datetime import datetime, timezone

def test_1987_case():
    engine = JyotishEngine()
    # August 22, 1987, 10:30 AM IST (Offset 5.5)
    # 10.5 hours - 5.5 = 5:00 UTC
    dt_utc = datetime(1987, 8, 22, 5, 0, tzinfo=timezone.utc)
    
    jd = engine.get_julian_day(dt_utc)
    print(f"Testing for Date: 1987-08-22 10:30 IST")
    print(f"Julian Day: {jd}")
    
    planets = engine.get_planetary_positions(jd)
    
    print("\nPlanetary Longitudes (Sidereal Lahiri):")
    for name, data in planets.items():
        print(f"{name:8}: {data['longitude']:10.4f}° | {data['sign']} {data['degree_in_sign']:8.4f}°")

    # Basic verification of expected signs (based on standard ephemeris for that date)
    # Sun in Leo, Moon in Cancer/Leo transition, Jupiter in Aries, etc.
    assert planets["Sun"]["sign"] == "Leo"
    print("\n✅ Verification Successful: Sun is in Leo as expected for Aug 1987.")

if __name__ == "__main__":
    test_1987_case()
