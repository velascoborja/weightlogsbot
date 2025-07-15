"""Main application file for the Telegram Weight Tracker Bot.

This bot tracks daily weight, sends weekly summaries, and monthly reports with charts.

Installation:
    python -m venv .venv && source .venv/bin/activate
    pip install "python-telegram-bot[rate-limiter]==21.1" matplotlib pytz

Usage:
    export TELEGRAM_TOKEN="<TU_TOKEN>"
    python main.py
"""

import signal
import sys
import asyncio
from telegram.ext import (
    AIORateLimiter,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    PicklePersistence,
)

from config import TOKEN, validate_config
from database import init_db
from backup_manager import restore_if_needed, auto_backup
from handlers import (
    start,
    help_cmd,
    peso_cmd,
    mensual_cmd,
    semanal_cmd,
    diario_cmd,
    numeric_listener,
    unknown_cmd,
)
from jobs import register_jobs


async def shutdown(app):
    """Graceful shutdown function."""
    print("🛑 Shutting down bot gracefully...")
    await app.stop()
    await app.shutdown()

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    print(f"📡 Received signal {signum}, shutting down...")
    sys.exit(0)

def main() -> None:
    """Initialize and run the Telegram bot."""
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Validate configuration
    validate_config()
    
    # Try to restore from backup if database doesn't exist
    restore_if_needed()
    
    # Initialize database
    init_db()

    # Set up persistence for jobs and user data
    persistence = PicklePersistence(filepath="bot_data.pkl")

    # Build application
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .persistence(persistence)
        .rate_limiter(AIORateLimiter())
        .build()
    )

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("peso", peso_cmd))
    app.add_handler(CommandHandler("mensual", mensual_cmd))
    app.add_handler(CommandHandler("semanal", semanal_cmd))
    app.add_handler(CommandHandler("diario", diario_cmd))

    # Add message handler for numeric input
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), numeric_listener))

    # Add handler for unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, unknown_cmd))

    # Start polling with graceful shutdown
    print("🤖 Bot started. Press Ctrl+C to stop.")
    try:
        app.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True,  # Ignore old messages during startup
            close_loop=False
        )
    except KeyboardInterrupt:
        print("🛑 Received interrupt signal, shutting down...")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
    finally:
        print("👋 Bot stopped.")


if __name__ == "__main__":
    main() 