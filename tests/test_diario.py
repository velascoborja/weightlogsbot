#!/usr/bin/env python3
"""Test script for the diario command functionality."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime as dt
from config import TZ
from database import get_weights, init_db, save_weight

def test_diario_logic():
    """Test the logic of the diario command without matplotlib."""
    print("Testing diario command logic...")
    
    # Initialize database
    init_db()
    
    # Simulate user_id
    user_id = 12345
    
    # Get today's date
    today = dt.datetime.now(TZ).date()
    
    # Get data for the last 6 days
    start_date = today - dt.timedelta(days=5)
    weights_data = get_weights(user_id, start_date, today)
    
    print(f"Date range: {start_date} to {today}")
    print(f"Weights data: {weights_data}")
    
    # Prepare text response
    lines = ["📆 Pesos últimos 6 días:"]
    for i in range(6):
        d = today - dt.timedelta(days=i)
        ws = get_weights(user_id, d, d)
        weight_text = f"{ws[0][1]:.1f} kg" if ws else "sin datos"
        lines.append(f"{d.strftime('%d/%m')}: {weight_text}")
    
    print("\nText response:")
    for line in lines:
        print(line)
    
    print(f"\nChart would be sent: {len(weights_data) >= 2}")

def test_with_sample_data():
    """Test with some sample weight data."""
    print("\n" + "="*50)
    print("Testing with sample data...")
    
    # Initialize database
    init_db()
    
    # Simulate user_id
    user_id = 54321
    
    # Add some sample weights
    today = dt.datetime.now(TZ).date()
    sample_weights = [
        (today - dt.timedelta(days=5), 72.5),
        (today - dt.timedelta(days=4), 72.3),
        (today - dt.timedelta(days=3), 72.8),
        (today - dt.timedelta(days=2), 72.1),
        (today - dt.timedelta(days=1), 71.9),
        (today, 72.0),
    ]
    
    for date, weight in sample_weights:
        save_weight(user_id, date, weight)
        print(f"Saved: {date} - {weight} kg")
    
    # Test diario command logic
    start_date = today - dt.timedelta(days=5)
    weights_data = get_weights(user_id, start_date, today)
    
    print(f"\nRetrieved data: {weights_data}")
    print(f"Chart would be sent: {len(weights_data) >= 2}")

if __name__ == "__main__":
    test_diario_logic()
    test_with_sample_data() 