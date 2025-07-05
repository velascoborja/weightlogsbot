"""Configuration settings for the Telegram Weight Tracker Bot."""

import os
import pytz

# Database configuration
DB_FILE = os.getenv("WEIGHT_DB", "weights.db")

# Bot configuration
TOKEN = os.getenv("TELEGRAM_TOKEN")
TZ = pytz.timezone(os.getenv("BOT_TZ", "Europe/Madrid"))
DAILY_HOUR = 8  # 08:00

# Validation
def validate_config():
    """Validate that all required configuration is present."""
    if not TOKEN:
        raise RuntimeError("Debes exportar TELEGRAM_TOKEN con tu token de BotFather") 