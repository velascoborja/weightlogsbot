"""Test script for the diario command without matplotlib."""

import datetime as dt
from config import TZ
from database import get_weights, init_db

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

if __name__ == "__main__":
    test_diario_logic() 