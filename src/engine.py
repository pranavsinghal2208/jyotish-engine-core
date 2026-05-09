import swisseph as swe
from datetime import datetime, timezone
from typing import Dict, List, Any

# Configure Swiss Ephemeris path if needed
# swe.set_ephe_path('./ephe') 
# By default, it uses the built-in ephemeris or look in current dir.

class JyotishEngine:
    def __init__(self, ayanamsa_id: int = swe.SIDM_LAHIRI):
        # Swiss Ephemeris uses built-in ephemeris files from pyswisseph package
        # No need to set ephe_path when using pyswisseph
        
        self.ayanamsa_id = ayanamsa_id
        # Set Sidereal Mode to Lahiri (or user specified)
        swe.set_sid_mode(self.ayanamsa_id, 0, 0)

    def get_julian_day(self, dt: datetime) -> float:
        """Convert a UTC datetime to Julian Day."""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        
        return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0 + dt.second/3600.0)

    def get_planetary_positions(self, jd_ut: float) -> Dict[str, Any]:
        """Calculate planetary positions for a given Julian Day in Sidereal Zodiac."""
        bodies = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mars": swe.MARS,
            "Mercury": swe.MERCURY,
            "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS,
            "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE,
            "Ketu": None 
        }
        
        results = {}
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
        
        for name, planet_id in bodies.items():
            if name == "Ketu":
                rahu_data = results["Rahu"]
                longitude = (rahu_data["longitude"] + 180) % 360
                results["Ketu"] = {
                    "longitude": longitude,
                    "speed": rahu_data["speed"],
                    "is_retrograde": True,
                    "sign": self.get_sign(longitude),
                    "degree_in_sign": longitude % 30
                }
                continue

            res, _ = swe.calc_ut(jd_ut, planet_id, flags)
            longitude = res[0]
            speed = res[3]
            results[name] = {
                "longitude": longitude,
                "speed": speed,
                "is_retrograde": speed < 0,
                "sign": self.get_sign(longitude),
                "degree_in_sign": longitude % 30
            }
        
        return results

    def get_houses(self, jd_ut: float, lat: float, lon: float) -> Dict[str, Any]:
        """Calculate houses and Ascendant (Lagna)."""
        # We use 'P' for Placidus or 'W' for Whole Sign. Jyotish usually uses Whole Sign or Sripati.
        # For simple Vedic, Whole Sign is common. 'W' is Whole Sign.
        # However, swe.houses() calculates tropical houses by default. 
        # For sidereal lagna, we need to subtract Ayanamsa or use a sidereal flag if supported.
        
        # Calculate Ayanamsa for the given JD
        ayanamsa = swe.get_ayanamsa_ex(jd_ut, swe.FLG_SIDEREAL)[1]
        
        # Calculate houses (using Whole Sign 'W')
        # swe.houses returns (cusps, ascmc)
        cusps, ascmc = swe.houses(jd_ut, lat, lon, b'W')
        
        # Lagna is the first element of ascmc (Ascendant)
        # Convert to Sidereal
        lagna_tropical = ascmc[0]
        lagna_sidereal = (lagna_tropical - ayanamsa) % 360
        
        return {
            "Lagna": {
                "longitude": lagna_sidereal,
                "sign": self.get_sign(lagna_sidereal),
                "degree_in_sign": lagna_sidereal % 30
            },
            "ayanamsa": ayanamsa
        }

    def get_sign(self, longitude: float) -> str:
        signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        return signs[int(longitude / 30)]

    def get_nakshatra(self, longitude: float) -> Dict[str, Any]:
        """Calculates Nakshatra name, lord, and Pada."""
        nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        
        nak_idx = int(longitude / (360/27))
        nak_name = nakshatras[nak_idx % 27]
        nak_lord = lords[nak_idx % 9]
        pada = int((longitude % (360/27)) / (360/108)) + 1
        
        return {
            "name": nak_name,
            "lord": nak_lord,
            "pada": pada,
            "longitude_in_nak": longitude % (360/27)
        }

    def get_vimshottari_dashas(self, moon_lon: float, birth_jd: float) -> List[Dict[str, Any]]:
        """Calculates the Vimshottari Dasha and nested Bhukti sequence."""
        lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        durations = [7, 20, 6, 10, 7, 18, 16, 19, 17]
        
        nak_span = 360/27
        nak_idx = int(moon_lon / nak_span)
        first_lord_idx = nak_idx % 9
        
        # Calculate balance of first dasha
        passed_in_nak = moon_lon % nak_span
        remaining_ratio = (nak_span - passed_in_nak) / nak_span
        
        first_md_duration = durations[first_lord_idx] * remaining_ratio
        
        dashas = []
        current_md_jd = birth_jd
        
        # Calculate for 120 years
        for i in range(9):
            md_lord_idx = (first_lord_idx + i) % 9
            md_lord = lords[md_lord_idx]
            md_duration_years = durations[md_lord_idx] if i > 0 else first_md_duration
            md_duration_jd = md_duration_years * 365.25
            
            md_start = swe.revjul(current_md_jd)
            md_end = swe.revjul(current_md_jd + md_duration_jd)
            
            # Calculate Bhuktis (Antar-Dashas) for this MD
            bhuktis = []
            current_ad_jd = current_md_jd
            
            # AD sequence starts from MD lord
            for j in range(9):
                ad_lord_idx = (md_lord_idx + j) % 9
                ad_lord = lords[ad_lord_idx]
                
                # Formula: (MD_years * AD_years) / 120
                ad_duration_years = (durations[md_lord_idx] * durations[ad_lord_idx]) / 120
                
                # Adjust first AD of the first MD based on remaining balance
                if i == 0 and j == 0:
                    ad_duration_years = ad_duration_years * remaining_ratio
                
                ad_duration_jd = ad_duration_years * 365.25
                ad_start = swe.revjul(current_ad_jd)
                ad_end = swe.revjul(current_ad_jd + ad_duration_jd)
                
                bhuktis.append({
                    "lord": ad_lord,
                    "start": f"{ad_start[0]}-{ad_start[1]:02d}-{ad_start[2]:02d}",
                    "end": f"{ad_end[0]}-{ad_end[1]:02d}-{ad_end[2]:02d}",
                    "duration": ad_duration_years
                })
                current_ad_jd += ad_duration_jd

            dashas.append({
                "lord": md_lord,
                "start": f"{md_start[0]}-{md_start[1]:02d}-{md_start[2]:02d}",
                "end": f"{md_end[0]}-{md_end[1]:02d}-{md_end[2]:02d}",
                "duration": md_duration_years,
                "bhuktis": bhuktis
            })
            
            current_md_jd += md_duration_jd
            
        return dashas

# Example usage
if __name__ == "__main__":
    engine = JyotishEngine()
    now = datetime.now(timezone.utc)
    jd = engine.get_julian_day(now)
    print(f"JD: {jd}")
    print(engine.get_planetary_positions(jd))
    print(engine.get_houses(jd, 28.6139, 77.2090)) # Delhi
