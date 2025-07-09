"""Main application file for the Telegram Weight Tracker Bot.

This bot tracks daily weight, sends weekly summaries, and monthly reports with charts.

Installation:
    python -m venv .venv && source .venv/bin/activate
    pip install "python-telegram-bot[rate-limiter]==21.1" matplotlib pytz

Usage:
    export TELEGRAM_TOKEN="<TU_TOKEN>"
    python main.py
"""

from telegram.ext import (
    AIORateLimiter,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TOKEN, validate_config
from database import init_db
from handlers import (
    start,
    help_cmd,
    peso_cmd,
    mensual_cmd,
    semanal_cmd,
    diario_cmd,
    numeric_listener,
)
from jobs import register_jobs


def main() -> None:
    """Initialize and run the Telegram bot."""
    # Validate configuration
    validate_config()
    
    # Initialize database
    init_db()

    # Build application
    app = (
        ApplicationBuilder()
        .token(TOKEN)
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

    # Start polling
    print("Bot started. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main() 