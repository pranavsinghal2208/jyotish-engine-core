#!/usr/bin/env python3
"""
Numerology Demo for Jyotish Engine Core
Test the numerology functionality with sample data.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from numerology import NumerologyEngine

def main():
    print("🌟 Jyotish Engine Core - Numerology Demo")
    print("=" * 50)
    
    engine = NumerologyEngine()
    
    # Sample data
    birth_date = "1990-05-15"
    full_name = "John Smith"
    
    print(f"📅 Birth Date: {birth_date}")
    print(f"👤 Full Name: {full_name}")
    print()
    
    # Get complete numerology reading
    print("🔮 Calculating Complete Numerology Reading...")
    result = engine.get_complete_numerology(birth_date, full_name)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    # Display results
    print("📊 LIFE PATH NUMBER:")
    life_path = result["life_path"]
    print(f"   Number: {life_path['life_path_number']}")
    print(f"   Month/Day Sum: {life_path['month_day_sum']}")
    print(f"   Interpretation: {life_path['interpretation']}")
    print()
    
    print("🎭 EXPRESSION NUMBER:")
    expression = result["expression"]
    print(f"   Number: {expression['expression_number']}")
    print(f"   Total Sum: {expression['total_sum']}")
    print(f"   Interpretation: {expression['interpretation']}")
    print()
    
    print("💫 SOUL URGE NUMBER:")
    soul_urge = result["soul_urge"]
    print(f"   Number: {soul_urge['soul_urge_number']}")
    print(f"   Vowels Used: {', '.join(soul_urge['vowel_letters'])}")
    print(f"   Interpretation: {soul_urge['interpretation']}")
    print()
    
    print("🎭 PERSONALITY NUMBER:")
    personality = result["personality"]
    print(f"   Number: {personality['personality_number']}")
    print(f"   Consonants Used: {', '.join(personality['consonant_letters'])}")
    print(f"   Interpretation: {personality['interpretation']}")
    print()
    
    print("⚖️ COMPATIBILITY ANALYSIS:")
    compatibility = result["compatibility"]
    print(f"   Score: {compatibility['score']}/100")
    print(f"   Level: {compatibility['level']}")
    print(f"   Life Path vs Expression: {compatibility['life_path']} vs {compatibility['expression']}")
    print()
    
    print("📝 NUMEROLOGY SUMMARY:")
    print(f"   {result['summary']}")
    print()
    
    print("✅ Numerology calculation complete!")
    print("\nTo integrate this into the web app:")
    print("1. The API endpoint /api/numerology is ready")
    print("2. Send POST request with birth_date and full_name")
    print("3. Add UI components to display the results")

if __name__ == "__main__":
    main()
