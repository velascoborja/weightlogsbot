"""Database operations for the Telegram Weight Tracker Bot."""

import datetime as dt
import sqlite3
from contextlib import closing
from typing import List, Tuple

from config import DB_FILE, DB_DIR


def init_db() -> None:
    """Initialize the database with the weights table."""
    # Create database directory if it doesn't exist
    import os
    os.makedirs(DB_DIR, exist_ok=True)
    
    with closing(sqlite3.connect(DB_FILE)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS weights (
                user_id INTEGER,
                date TEXT,
                weight REAL,
                PRIMARY KEY (user_id, date)
            )
            """
        )
        conn.commit()


def save_weight(user_id: int, date: dt.date, weight: float) -> None:
    """Save a weight entry for a user on a specific date."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        conn.execute(
            "REPLACE INTO weights (user_id, date, weight) VALUES (?,?,?)",
            (user_id, date.isoformat(), weight),
        )
        conn.commit()


def get_weights(user_id: int, start: dt.date, end: dt.date) -> List[Tuple[dt.date, float]]:
    """Get weight entries for a user within a date range."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        cur = conn.execute(
            "SELECT date, weight FROM weights WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date",
            (user_id, start.isoformat(), end.isoformat()),
        )
        rows = cur.fetchall()
    return [(dt.date.fromisoformat(d), w) for d, w in rows]


def _month_end(date_: dt.date) -> dt.date:
    """Get the last day of the month for a given date."""
    next_month = date_.replace(day=28) + dt.timedelta(days=4)
    return next_month.replace(day=1) - dt.timedelta(days=1)


def get_monthly_weights(user_id: int, months_back: int = 6) -> List[Tuple[str, float]]:
    """Get monthly average weights for the last N months."""
    today = dt.datetime.now().date()
    results = []
    
    for offset in range(0, months_back):
        tot = today.year * 12 + today.month - 1 - offset
        year, month = divmod(tot, 12)
        month += 1
        start = dt.date(year, month, 1)
        end = _month_end(start)
        ws = get_weights(user_id, start, end)
        
        month_name = start.strftime('%b %Y')
        avg_weight = sum(w for _, w in ws) / len(ws) if ws else None
        results.append((month_name, avg_weight))
    
    return results


def get_weekly_weights(user_id: int, weeks_back: int = 4) -> List[Tuple[str, float]]:
    """Get weekly average weights for the last N weeks."""
    today = dt.datetime.now().date()
    monday = today - dt.timedelta(days=today.weekday())
    results = []
    
    for i in range(0, weeks_back):
        start = monday - dt.timedelta(days=7 * i)
        end = start + dt.timedelta(days=6)
        ws = get_weights(user_id, start, end)
        
        span = f"{start.strftime('%d/%m')}–{end.strftime('%d/%m')}"
        avg_weight = sum(w for _, w in ws) / len(ws) if ws else None
        results.append((span, avg_weight))
    
    return results


def get_daily_weights(user_id: int, days_back: int = 6) -> List[Tuple[str, float]]:
    """Get daily weights for the last N days."""
    today = dt.datetime.now().date()
    results = []
    
    for i in range(0, days_back):
        d = today - dt.timedelta(days=i)
        ws = get_weights(user_id, d, d)
        
        date_str = d.strftime('%d/%m')
        weight = ws[-1][1] if ws else None
        results.append((date_str, weight))
    
    return results 