#!/usr/bin/env python3
"""Test script for internationalization strings."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lang.strings import get_strings

def test_i18n_strings():
    """Test that all new i18n strings work correctly."""
    print("Testing internationalization strings...")
    
    # Test Spanish strings
    strings_es = get_strings('es')
    print("\n=== Spanish Strings ===")
    print(f"Weekly summary header: {strings_es['weekly_summary_header']}")
    print(f"Weekly no change: {strings_es['weekly_no_change']}")
    print(f"Weekly decrease: {strings_es['weekly_decrease'].format(diff=2.5)}")
    print(f"Weekly increase: {strings_es['weekly_increase'].format(diff=1.3)}")
    print(f"Monthly no change: {strings_es['monthly_no_change']}")
    print(f"Monthly decrease: {strings_es['monthly_decrease'].format(diff=3.2)}")
    print(f"Monthly increase: {strings_es['monthly_increase'].format(diff=1.8)}")
    print(f"Daily reminder: {strings_es['daily_reminder']}")
    
    # Test English strings
    strings_en = get_strings('en')
    print("\n=== English Strings ===")
    print(f"Weekly summary header: {strings_en['weekly_summary_header']}")
    print(f"Weekly no change: {strings_en['weekly_no_change']}")
    print(f"Weekly decrease: {strings_en['weekly_decrease'].format(diff=2.5)}")
    print(f"Weekly increase: {strings_en['weekly_increase'].format(diff=1.3)}")
    print(f"Monthly no change: {strings_en['monthly_no_change']}")
    print(f"Monthly decrease: {strings_en['monthly_decrease'].format(diff=3.2)}")
    print(f"Monthly increase: {strings_en['monthly_increase'].format(diff=1.8)}")
    print(f"Daily reminder: {strings_en['daily_reminder']}")
    
    # Test weekly summary format
    print("\n=== Sample Weekly Summary ===")
    weekly_format = strings_es['weekly_summary_format'].format(
        current=72.5, 
        previous=73.0, 
        change=strings_es['weekly_decrease'].format(diff=0.5)
    )
    print(f"Spanish: {strings_es['weekly_summary_header']}")
    print(f"         {weekly_format}")
    
    weekly_format_en = strings_en['weekly_summary_format'].format(
        current=72.5, 
        previous=73.0, 
        change=strings_en['weekly_decrease'].format(diff=0.5)
    )
    print(f"English: {strings_en['weekly_summary_header']}")
    print(f"         {weekly_format_en}")
    
    # Test monthly summary format
    print("\n=== Sample Monthly Summary ===")
    monthly_format = strings_es['monthly_summary_format'].format(
        month="Ago 2025",
        start=74.0,
        end=72.0,
        change=strings_es['monthly_decrease'].format(diff=2.0)
    )
    print(f"Spanish: {monthly_format}")
    
    monthly_format_en = strings_en['monthly_summary_format'].format(
        month="Aug 2025",
        start=74.0,
        end=72.0,
        change=strings_en['monthly_decrease'].format(diff=2.0)
    )
    print(f"English: {monthly_format_en}")
    
    print("\n✅ All i18n strings work correctly!")
    return True

if __name__ == "__main__":
    try:
        test_i18n_strings()
        print("\n🎉 i18n test passed!")
    except Exception as e:
        print(f"\n❌ i18n test failed: {e}")
        sys.exit(1)
