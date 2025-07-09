"""Configuration settings for the Telegram Weight Tracker Bot."""

import os
import pytz

# Database configuration
# Use a directory that Railway preserves between deploys
DB_DIR = os.getenv("WEIGHT_DB_DIR", "/tmp")
DB_FILE = os.path.join(DB_DIR, os.getenv("WEIGHT_DB_NAME", "weights.db"))

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Bot configuration
TOKEN = os.getenv("TELEGRAM_TOKEN")
TZ = pytz.timezone(os.getenv("BOT_TZ", "Europe/Madrid"))
DAILY_HOUR = 8  # 08:00

# Validation
def validate_config():
    """Validate that all required configuration is present."""
    if not TOKEN:
        raise RuntimeError("Debes exportar TELEGRAM_TOKEN con tu token de BotFather") 