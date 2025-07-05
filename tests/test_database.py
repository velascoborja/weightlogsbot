#!/usr/bin/env python3
"""Test script for database operations."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime as dt
from database import (
    init_db, 
    save_weight, 
    get_weights, 
    get_monthly_weights, 
    get_weekly_weights, 
    get_daily_weights
)

def test_basic_operations():
    """Test basic database operations."""
    print("Testing basic database operations...")
    
    # Initialize database
    init_db()
    print("✓ Database initialized")
    
    # Test user
    user_id = 99999
    
    # Test save and retrieve
    test_date = dt.date.today()
    test_weight = 75.5
    
    save_weight(user_id, test_date, test_weight)
    print(f"✓ Weight saved: {test_weight} kg on {test_date}")
    
    # Retrieve the weight
    weights = get_weights(user_id, test_date, test_date)
    if weights and weights[0][1] == test_weight:
        print("✓ Weight retrieved correctly")
    else:
        print("✗ Weight retrieval failed")
        return False
    
    return True

def test_multiple_weights():
    """Test saving and retrieving multiple weights."""
    print("\nTesting multiple weights...")
    
    user_id = 88888
    today = dt.date.today()
    
    # Save multiple weights
    test_weights = [
        (today - dt.timedelta(days=5), 74.0),
        (today - dt.timedelta(days=4), 73.8),
        (today - dt.timedelta(days=3), 74.2),
        (today - dt.timedelta(days=2), 73.9),
        (today - dt.timedelta(days=1), 73.7),
        (today, 73.5),
    ]
    
    for date, weight in test_weights:
        save_weight(user_id, date, weight)
        print(f"✓ Saved: {date} - {weight} kg")
    
    # Test retrieval
    start_date = today - dt.timedelta(days=5)
    weights = get_weights(user_id, start_date, today)
    
    if len(weights) == 6:
        print(f"✓ Retrieved {len(weights)} weights correctly")
    else:
        print(f"✗ Expected 6 weights, got {len(weights)}")
        return False
    
    return True

def test_aggregate_functions():
    """Test monthly, weekly, and daily aggregate functions."""
    print("\nTesting aggregate functions...")
    
    user_id = 77777
    today = dt.date.today()
    
    # Add some sample data for the last month
    for i in range(30):
        date = today - dt.timedelta(days=i)
        weight = 70.0 + (i % 5) * 0.5  # Varying weight
        save_weight(user_id, date, weight)
    
    # Test monthly weights
    monthly = get_monthly_weights(user_id, months_back=3)
    print(f"✓ Monthly weights: {len(monthly)} months")
    
    # Test weekly weights
    weekly = get_weekly_weights(user_id, weeks_back=4)
    print(f"✓ Weekly weights: {len(weekly)} weeks")
    
    # Test daily weights
    daily = get_daily_weights(user_id, days_back=6)
    print(f"✓ Daily weights: {len(daily)} days")
    
    return True

def main():
    """Run all database tests."""
    print("=== Database Test Suite ===\n")
    
    tests = [
        ("Basic Operations", test_basic_operations),
        ("Multiple Weights", test_multiple_weights),
        ("Aggregate Functions", test_aggregate_functions),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} passed")
            else:
                print(f"✗ {test_name} failed")
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
    
    print(f"\n=== Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All database tests passed!")
    else:
        print("❌ Some database tests failed.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 