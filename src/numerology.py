"""
Numerology calculations for Jyotish Engine Core.
Calculates Life Path Number, Expression Number, Soul Urge Number, and Personality Number.
Also includes Jyotish-style calculations: Mulank, Bhagyank, Gift#, KUA, Lo Shu Grid.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from .numerology_data import (
    DRIVER_CONDUCTOR_PROFILES, MISSING_NUMBER_REMEDIES,
    NUMBER_MEANINGS, LO_SHU_POSITIONS, KARMIC_NUMBERS,
    NAMANK_INTERPRETATIONS, LOTTERY_NUMBER_MEANINGS
)


class NumerologyEngine:
    """Engine for calculating numerological values from birth details."""
    
    def __init__(self):
        # Chaldean number mapping
        self.chaldean_map = {
            'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
            'B': 2, 'K': 2, 'R': 2,
            'C': 3, 'G': 3, 'L': 3, 'S': 3,
            'D': 4, 'M': 4, 'T': 4,
            'E': 5, 'H': 5, 'N': 5, 'X': 5,
            'U': 6, 'V': 6, 'W': 6,
            'O': 7, 'Z': 7,
            'F': 8, 'P': 8
        }
        
        # Pythagorean number mapping (alternative)
        self.pythagorean_map = {
            'A': 1, 'J': 1, 'S': 1,
            'B': 2, 'K': 2, 'T': 2,
            'C': 3, 'L': 3, 'U': 3,
            'D': 4, 'M': 4, 'V': 4,
            'E': 5, 'N': 5, 'W': 5,
            'F': 6, 'O': 6, 'X': 6,
            'G': 7, 'P': 7, 'Y': 7,
            'H': 8, 'Q': 8, 'Z': 8,
            'I': 9, 'R': 9
        }
    
    def reduce_to_single_digit(self, number: int) -> int:
        """Reduce a number to a single digit (1-9), except master numbers 11, 22, 33."""
        if number in [11, 22, 33]:
            return number
        while number > 9:
            number = sum(int(digit) for digit in str(number))
        return number
    
    def calculate_life_path_number(self, birth_date: str) -> Dict[str, Any]:
        """Calculate Life Path Number from birth date."""
        try:
            date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
            day = date_obj.day
            month = date_obj.month
            year = date_obj.year
            
            # Sum all digits
            total = day + month + year
            life_path = self.reduce_to_single_digit(total)
            
            # Calculate month/day variations
            month_day_sum = self.reduce_to_single_digit(day + month)
            
            return {
                "life_path_number": life_path,
                "month_day_sum": month_day_sum,
                "total_sum": total,
                "interpretation": self.get_life_path_interpretation(life_path)
            }
        except Exception as e:
            return {"error": f"Invalid date format: {str(e)}"}
    
    def calculate_expression_number(self, full_name: str) -> Dict[str, Any]:
        """Calculate Expression Number from full name."""
        try:
            # Remove spaces and convert to uppercase
            name = ''.join(full_name.split()).upper()
            
            total = 0
            letter_values = {}
            
            for letter in name:
                if letter in self.chaldean_map:
                    value = self.chaldean_map[letter]
                    letter_values[letter] = value
                    total += value
            
            expression_number = self.reduce_to_single_digit(total)
            
            return {
                "expression_number": expression_number,
                "total_sum": total,
                "letter_values": letter_values,
                "interpretation": self.get_expression_interpretation(expression_number)
            }
        except Exception as e:
            return {"error": f"Error calculating expression number: {str(e)}"}
    
    def calculate_soul_urge_number(self, vowels_only: str) -> Dict[str, Any]:
        """Calculate Soul Urge Number from vowels in name."""
        try:
            vowels = "AEIOU"
            vowel_letters = [letter for letter in vowels_only.upper() if letter in vowels]
            
            total = 0
            letter_values = {}
            
            for letter in vowel_letters:
                if letter in self.chaldean_map:
                    value = self.chaldean_map[letter]
                    letter_values[letter] = value
                    total += value
            
            soul_urge = self.reduce_to_single_digit(total)
            
            return {
                "soul_urge_number": soul_urge,
                "total_sum": total,
                "vowel_letters": vowel_letters,
                "letter_values": letter_values,
                "interpretation": self.get_soul_urge_interpretation(soul_urge)
            }
        except Exception as e:
            return {"error": f"Error calculating soul urge number: {str(e)}"}
    
    def calculate_personality_number(self, consonants_only: str) -> Dict[str, Any]:
        """Calculate Personality Number from consonants in name."""
        try:
            vowels = "AEIOU"
            consonant_letters = [letter for letter in consonants_only.upper() if letter not in vowels and letter.isalpha()]
            
            total = 0
            letter_values = {}
            
            for letter in consonant_letters:
                if letter in self.chaldean_map:
                    value = self.chaldean_map[letter]
                    letter_values[letter] = value
                    total += value
            
            personality = self.reduce_to_single_digit(total)
            
            return {
                "personality_number": personality,
                "total_sum": total,
                "consonant_letters": consonant_letters,
                "letter_values": letter_values,
                "interpretation": self.get_personality_interpretation(personality)
            }
        except Exception as e:
            return {"error": f"Error calculating personality number: {str(e)}"}
    
    def get_complete_numerology(self, birth_date: str, full_name: str) -> Dict[str, Any]:
        """Get complete numerology reading combining all calculations."""
        try:
            life_path = self.calculate_life_path_number(birth_date)
            expression = self.calculate_expression_number(full_name)
            
            # Extract vowels and consonants for soul urge and personality
            vowels = "AEIOU"
            vowels_only = ''.join([c for c in full_name.upper() if c in vowels])
            consonants_only = ''.join([c for c in full_name.upper() if c not in vowels and c.isalpha()])
            
            soul_urge = self.calculate_soul_urge_number(vowels_only)
            personality = self.calculate_personality_number(consonants_only)
            
            # Calculate compatibility between numbers
            compatibility = self.calculate_compatibility(life_path.get("life_path_number", 0), 
                                                       expression.get("expression_number", 0))
            
            return {
                "life_path": life_path,
                "expression": expression,
                "soul_urge": soul_urge,
                "personality": personality,
                "compatibility": compatibility,
                "summary": self.generate_numerology_summary(life_path, expression, soul_urge, personality)
            }
        except Exception as e:
            return {"error": f"Error generating complete numerology: {str(e)}"}
    
    def calculate_compatibility(self, life_path: int, expression: int) -> Dict[str, Any]:
        """Calculate compatibility between Life Path and Expression numbers."""
        if life_path == expression:
            compatibility_score = 100
            compatibility_level = "Perfect Harmony"
        elif abs(life_path - expression) <= 2:
            compatibility_score = 85
            compatibility_level = "Strong Compatibility"
        elif abs(life_path - expression) <= 4:
            compatibility_score = 70
            compatibility_level = "Good Compatibility"
        else:
            compatibility_score = 55
            compatibility_level = "Challenging Combination"
        
        return {
            "score": compatibility_score,
            "level": compatibility_level,
            "life_path": life_path,
            "expression": expression,
            "difference": abs(life_path - expression)
        }
    
    def generate_numerology_summary(self, life_path: Dict, expression: Dict, soul_urge: Dict, personality: Dict) -> str:
        """Generate a comprehensive numerology summary."""
        try:
            lp_num = life_path.get("life_path_number", 0)
            exp_num = expression.get("expression_number", 0)
            soul_num = soul_urge.get("soul_urge_number", 0)
            pers_num = personality.get("personality_number", 0)
            
            summary = f"Your numerology profile reveals a Life Path {lp_num} individual "
            summary += f"with Expression Number {exp_num}, indicating "
            
            if lp_num == exp_num:
                summary += "perfect alignment between your life's purpose and natural talents. "
            else:
                summary += f"a dynamic tension between purpose (Life Path {lp_num}) and expression (Number {exp_num}). "
            
            summary += f"Your Soul Urge Number {soul_num} shows your deepest desires and motivations, "
            summary += f"while your Personality Number {pers_num} represents how others perceive you."
            
            return summary
        except:
            return "Unable to generate numerology summary due to calculation errors."
    
    # Interpretation methods (simplified versions)
    def get_life_path_interpretation(self, number: int) -> str:
        interpretations = {
            1: "Leadership, independence, and pioneering spirit.",
            2: "Cooperation, diplomacy, and partnership.",
            3: "Creativity, communication, and self-expression.",
            4: "Stability, organization, and hard work.",
            5: "Freedom, adventure, and versatility.",
            6: "Responsibility, nurturing, and harmony.",
            7: "Analysis, introspection, and spirituality.",
            8: "Power, ambition, and material success.",
            9: "Humanitarianism, compassion, and completion."
        }
        return interpretations.get(number, "Unique path requiring personal exploration.")
    
    def get_expression_interpretation(self, number: int) -> str:
        interpretations = {
            1: "Natural leader with strong individuality.",
            2: "Diplomatic mediator and team player.",
            3: "Creative communicator and artist.",
            4: "Practical builder and organizer.",
            5: "Versatile adventurer and communicator.",
            6: "Caring nurturer and responsible guardian.",
            7: "Analytical thinker and spiritual seeker.",
            8: "Ambitious achiever and authority figure.",
            9: "Compassionate humanitarian and visionary."
        }
        return interpretations.get(number, "Unique expression of talents and abilities.")
    
    def get_soul_urge_interpretation(self, number: int) -> str:
        interpretations = {
            1: "Deep desire for independence and leadership.",
            2: "Need for partnership and harmonious relationships.",
            3: "Inner drive for creative self-expression.",
            4: "Longing for stability and practical achievement.",
            5: "Craving freedom and new experiences.",
            6: "Desire to nurture and care for others.",
            7: "Inner need for knowledge and spiritual growth.",
            8: "Ambition for success and material security.",
            9: "Compassion for humanity and desire to help others."
        }
        return interpretations.get(number, "Unique inner motivations and desires.")
    
    def get_personality_interpretation(self, number: int) -> str:
        interpretations = {
            1: "Appears confident, independent, and decisive.",
            2: "Seems diplomatic, cooperative, and sensitive.",
            3: "Looks creative, expressive, and optimistic.",
            4: "Appears practical, reliable, and hardworking.",
            5: "Seems adventurous, versatile, and freedom-loving.",
            6: "Appears responsible, caring, and harmonious.",
            7: "Looks analytical, introspective, and spiritual.",
            8: "Appears ambitious, authoritative, and successful.",
            9: "Seems compassionate, generous, and idealistic."
        }
        return interpretations.get(number, "Unique outward personality and presentation.")

    # ------------------------------------------------------------------
    # Jyotish-style numerology (matches the master sheet)
    # ------------------------------------------------------------------

    def _parse_dob(self, dob: str) -> datetime:
        """Parse DD-MM-YYYY or DD-Mon-YYYY or YYYY-MM-DD into a datetime."""
        for fmt in ("%d-%m-%Y", "%d-%b-%Y", "%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(dob.strip(), fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognised DOB format: {dob}")

    def _jyotish_reduce(self, n: int) -> int:
        """Reduce to single digit — no master-number exceptions (sheet style)."""
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    def calculate_mulank(self, dob: str) -> int:
        """Driver number: birth day reduced to single digit."""
        day = self._parse_dob(dob).day
        return self._jyotish_reduce(day)

    def calculate_gift_number(self, dob: str) -> int:
        """Raw sum of all individual digits in DD-MM-YYYY (before final reduction)."""
        dt = self._parse_dob(dob)
        raw = f"{dt.day:02d}{dt.month:02d}{dt.year:04d}"
        return sum(int(c) for c in raw)

    def calculate_bhagyank(self, dob: str) -> int:
        """Conductor / life-path: gift number reduced to single digit."""
        return self._jyotish_reduce(self.calculate_gift_number(dob))

    def calculate_birth_year_number(self, dob: str) -> int:
        year = self._parse_dob(dob).year
        return self._jyotish_reduce(sum(int(c) for c in str(year)))

    def calculate_kua_number(self, dob: str, gender: str) -> int:
        """Feng Shui KUA number."""
        dt = self._parse_dob(dob)
        year_sum = self._jyotish_reduce(sum(int(c) for c in str(dt.year)))
        if dt.year >= 2000:
            kua = (year_sum + 2) if gender.lower() == "male" else (year_sum + 8)
        else:
            kua = (11 - year_sum) if gender.lower() == "male" else (year_sum + 4)
        return self._jyotish_reduce(kua) or 9

    def calculate_namank(self, first: str, middle: str, last: str) -> int:
        """Chaldean name number from all non-empty name parts concatenated."""
        full = "".join(part.upper() for part in [first, middle, last] if part)
        total = sum(self.chaldean_map.get(c, 0) for c in full if c.isalpha())
        return self._jyotish_reduce(total) if total else 0

    def calculate_lo_shu_grid(self, dob: str, mulank: int = None, bhagyank: int = None) -> Dict[str, Any]:
        """
        Returns which digits (1–9) are present / missing in the DOB,
        plus Mulank and Bhagyank for the complete 'Osho' style grid.
        """
        dt = self._parse_dob(dob)
        raw = f"{dt.day:02d}{dt.month:02d}{dt.year:04d}"
        freq: Dict[int, int] = {n: 0 for n in range(1, 10)}
        for c in raw:
            if c != "0":
                freq[int(c)] = freq.get(int(c), 0) + 1
        
        # In Jyotish/Osho style, Driver and Conductor also populate the grid
        if mulank: freq[mulank] = freq.get(mulank, 0) + 1
        if bhagyank: freq[bhagyank] = freq.get(bhagyank, 0) + 1

        present = {n: cnt for n, cnt in freq.items() if cnt > 0}
        missing = [n for n, cnt in freq.items() if cnt == 0]

        grid = [[None, None, None] for _ in range(3)]
        for num, (r, c) in LO_SHU_POSITIONS.items():
            grid[r][c] = {"number": num, "count": freq[num]}

        return {"present": present, "missing": missing, "grid": grid}

    def get_driver_conductor_profile(self, driver: int, conductor: int) -> Optional[Dict]:
        return DRIVER_CONDUCTOR_PROFILES.get(f"{driver}~{conductor}")

    def get_missing_remedies(self, missing_numbers: List[int]) -> List[Dict]:
        return [
            {"number": n, **MISSING_NUMBER_REMEDIES[n]}
            for n in missing_numbers if n in MISSING_NUMBER_REMEDIES
        ]

    # ── Personal Cycle interpretations ────────────────────────────────────────
    _CYCLE_THEMES = {
        1: {"theme": "New Beginnings",     "energy": "Pioneer",     "focus": "Launch new ventures, assert independence, and initialize 9-year cycle seeds."},
        2: {"theme": "Partnership",        "energy": "Diplomat",    "focus": "Nurture relationships and collaborate. Optimized for support and alignment."},
        3: {"theme": "Expression",         "energy": "Creator",     "focus": "High social ROI. Prioritize communication, networking, and creative visibility."},
        4: {"theme": "Foundation",         "energy": "Builder",     "focus": "Systems-build window. Prioritize structure and rigorous execution. ROI is lagging."},
        5: {"theme": "Change",             "energy": "Adventurer",  "focus": "High volatility window. Pivot-ready mindset required. Freedom and adaptation ROI."},
        6: {"theme": "Responsibility",     "energy": "Caretaker",   "focus": "Domestic scaling and service. Deepen commitments and optimize home-infrastructure."},
        7: {"theme": "Reflection",         "energy": "Seeker",      "focus": "Process-audit window. Retreat and introspect. Focus on analytical or spiritual rigor."},
        8: {"theme": "Achievement",        "energy": "Executive",   "focus": "High-stakes execution. Leverage power and ambition for material scaling. Execute now."},
        9: {"theme": "Completion",         "energy": "Humanitarian","focus": "Cycle-closure. Release non-essential commitments to clear bandwidth for Year 1."},
    }

    def get_personal_cycles(self, dob: str, current_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Personal Year, Month, and Day numbers from Bhagyank + current date."""
        today = current_date or datetime.utcnow()
        bhagyank = self.calculate_bhagyank(dob)

        universal_year  = self._jyotish_reduce(sum(int(c) for c in str(today.year)))
        personal_year   = self._jyotish_reduce(bhagyank + universal_year)
        personal_month  = self._jyotish_reduce(personal_year + today.month)
        personal_day    = self._jyotish_reduce(personal_month + today.day)

        def _enrich(num):
            t = self._CYCLE_THEMES.get(num, {})
            m = NUMBER_MEANINGS.get(num, {})
            return {
                "number": num,
                "theme": t.get("theme", ""),
                "energy": t.get("energy", ""),
                "focus": t.get("focus", ""),
                "planet": m.get("planet", ""),
                "color":  m.get("color", ""),
            }

        return {
            "bhagyank": bhagyank,
            "universal_year": universal_year,
            "personal_year":  _enrich(personal_year),
            "personal_month": _enrich(personal_month),
            "personal_day":   _enrich(personal_day),
            "date": today.strftime("%Y-%m-%d"),
        }

    def get_two_person_compatibility(self, profile_a: Dict, profile_b: Dict) -> Dict[str, Any]:
        """Compare two Jyotish profiles and return compatibility analysis."""
        ma, ba = profile_a["mulank"], profile_a["bhagyank"]
        mb, bb = profile_b["mulank"], profile_b["bhagyank"]

        # DC score: how each person's DC pair scores against the other person's Driver
        dc_ab = DRIVER_CONDUCTOR_PROFILES.get(f"{ma}~{bb}", {})  # A drives, B conducts
        dc_ba = DRIVER_CONDUCTOR_PROFILES.get(f"{mb}~{ba}", {})  # B drives, A conducts

        score_ab = dc_ab.get("compatibility", 0)
        score_ba = dc_ba.get("compatibility", 0)
        avg_score = round((score_ab + score_ba) / 2)

        # Number resonance: shared strengths/tensions
        shared_driver = ma == mb
        shared_conductor = ba == bb
        same_planet_driver = NUMBER_MEANINGS.get(ma, {}).get("planet") == NUMBER_MEANINGS.get(mb, {}).get("planet")

        if avg_score >= 80:
            verdict = "High Resonance"
            verdict_color = "green"
        elif avg_score >= 65:
            verdict = "Compatible"
            verdict_color = "blue"
        elif avg_score >= 50:
            verdict = "Moderate Tension"
            verdict_color = "amber"
        else:
            verdict = "Challenging"
            verdict_color = "red"

        return {
            "score": avg_score,
            "verdict": verdict,
            "verdict_color": verdict_color,
            "person_a": {"mulank": ma, "bhagyank": ba,
                         "driver_planet": NUMBER_MEANINGS.get(ma, {}).get("planet", ""),
                         "conductor_planet": NUMBER_MEANINGS.get(ba, {}).get("planet", "")},
            "person_b": {"mulank": mb, "bhagyank": bb,
                         "driver_planet": NUMBER_MEANINGS.get(mb, {}).get("planet", ""),
                         "conductor_planet": NUMBER_MEANINGS.get(bb, {}).get("planet", "")},
            "dynamics": {
                "a_leads_b": {"score": score_ab, "pros": dc_ab.get("pros", [])[:3], "cons": dc_ab.get("cons", [])[:2]},
                "b_leads_a": {"score": score_ba, "pros": dc_ba.get("pros", [])[:3], "cons": dc_ba.get("cons", [])[:2]},
            },
            "shared": {
                "same_driver": shared_driver,
                "same_conductor": shared_conductor,
                "same_planet": same_planet_driver,
            },
            "summary": (
                f"Driver {ma} ({NUMBER_MEANINGS.get(ma,{}).get('planet','')}) interaction with Driver {mb} ({NUMBER_MEANINGS.get(mb,{}).get('planet','')}). "
                f"Pairing efficiency: {avg_score}/100 — {verdict}."
            )
        }

    def get_yearly_forecast(self, dob: str, year: int) -> Dict[str, Any]:
        """12-month numerology forecast for a given year."""
        bhagyank = self.calculate_bhagyank(dob)
        universal_year = self._jyotish_reduce(sum(int(c) for c in str(year)))
        personal_year = self._jyotish_reduce(bhagyank + universal_year)
        py_info = self._CYCLE_THEMES.get(personal_year, {})
        py_meaning = NUMBER_MEANINGS.get(personal_year, {})

        months = []
        for m in range(1, 13):
            pm = self._jyotish_reduce(personal_year + m)
            pm_info = self._CYCLE_THEMES.get(pm, {})
            pm_meaning = NUMBER_MEANINGS.get(pm, {})
            months.append({
                "month": m,
                "month_name": datetime(year, m, 1).strftime("%B"),
                "personal_month": pm,
                "theme": pm_info.get("theme", ""),
                "energy": pm_info.get("energy", ""),
                "focus": pm_info.get("focus", ""),
                "planet": pm_meaning.get("planet", ""),
                "color": pm_meaning.get("color", ""),
            })

        action_months = [mo for mo in months if mo["personal_month"] in (1, 3, 8)]
        rest_months   = [mo for mo in months if mo["personal_month"] in (7, 9)]

        return {
            "year": year,
            "bhagyank": bhagyank,
            "universal_year": universal_year,
            "personal_year": {
                "number": personal_year,
                "theme": py_info.get("theme", ""),
                "energy": py_info.get("energy", ""),
                "focus": py_info.get("focus", ""),
                "planet": py_meaning.get("planet", ""),
                "color": py_meaning.get("color", ""),
            },
            "months": months,
            "highlights": {
                "action_months": [m["month_name"] for m in action_months],
                "rest_months":   [m["month_name"] for m in rest_months],
            },
        }

    def calculate_lottery_numbers(self, mulank: int, bhagyank: int, kua: int) -> Dict[str, Any]:
        """Logic for identifying 'Lottery' or 'Universal Luck' numbers."""
        # Primary luck is usually Mulank + KUA interaction
        primary = self._jyotish_reduce(mulank + kua)
        # Secondary is often Bhagyank (destiny)
        secondary = bhagyank
        
        return {
            "primary": {
                "number": primary,
                "label": "Universal Luck",
                "meaning": LOTTERY_NUMBER_MEANINGS["primary"]
            },
            "secondary": {
                "number": secondary,
                "label": "Financial Flow",
                "meaning": LOTTERY_NUMBER_MEANINGS["secondary"]
            }
        }

    def get_jyotish_profile(
        self, dob: str, first_name: str, middle_name: str, last_name: str, gender: str
    ) -> Dict[str, Any]:
        """Complete Jyotish numerology profile matching the master sheet."""
        try:
            mulank = self.calculate_mulank(dob)
            gift = self.calculate_gift_number(dob)
            bhagyank = self.calculate_bhagyank(dob)
            namank = self.calculate_namank(first_name, middle_name, last_name)
            birth_year_num = self.calculate_birth_year_number(dob)
            kua = self.calculate_kua_number(dob, gender)
            
            # Audit: Pass Mulank and Bhagyank into Lo Shu calculation
            lo_shu = self.calculate_lo_shu_grid(dob, mulank, bhagyank)
            
            dc_profile = self.get_driver_conductor_profile(mulank, bhagyank)
            missing_remedies = self.get_missing_remedies(lo_shu["missing"])
            
            # New: Lottery Numbers
            lottery = self.calculate_lottery_numbers(mulank, bhagyank, kua)

            return {
                "mulank": mulank,
                "gift_number": gift,
                "bhagyank": bhagyank,
                "namank": {
                    "number": namank,
                    "meaning": NAMANK_INTERPRETATIONS.get(namank, "Unique name vibration.")
                },
                "birth_year_number": birth_year_num,
                "kua_number": kua,
                "lottery_numbers": lottery,
                "lo_shu_grid": lo_shu,
                "driver_conductor_profile": dc_profile,
                "missing_remedies": missing_remedies,
                "number_meanings": {
                    n: NUMBER_MEANINGS[n]
                    for n in lo_shu["present"] if n in NUMBER_MEANINGS
                },
                "karmic_numbers": KARMIC_NUMBERS,
            }
        except Exception as e:
            return {"error": str(e)}
