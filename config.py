"""Configuration settings for the Telegram Weight Tracker Bot."""

import os
import pytz

# Database configuration
# Use a directory within the project that Railway preserves
DB_DIR = os.getenv("WEIGHT_DB_DIR", "data")
DB_FILE = os.path.join(DB_DIR, os.getenv("WEIGHT_DB_NAME", "weights.db"))

# Bot configuration
TOKEN = os.getenv("TELEGRAM_TOKEN")
TZ = pytz.timezone(os.getenv("BOT_TZ", "Europe/Madrid"))
DAILY_HOUR = 8  # 08:00

# Validation
def validate_config():
    """Validate that all required configuration is present."""
    if not TOKEN:
        raise RuntimeError("Debes exportar TELEGRAM_TOKEN con tu token de BotFather") 