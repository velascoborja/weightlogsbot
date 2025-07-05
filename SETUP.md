# Local Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- A Telegram bot token (get from @BotFather)

## Step-by-Step Setup

### 1. Clone or Download the Project
```bash
git clone <your-repo-url>
cd weightlogs
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 5. Set Environment Variables
```bash
# Set your bot token
export TELEGRAM_TOKEN="your_bot_token_here"

# Optional: Set timezone (default: Europe/Madrid)
export BOT_TZ="America/New_York"

# Optional: Set custom database file (default: weights.db)
export WEIGHT_DB="my_weights.db"
```

### 6. Run the Bot
```bash
python main.py
```

You should see: `Bot started. Press Ctrl+C to stop.`

### 7. Test the Bot
1. Open Telegram
2. Search for your bot username
3. Send `/start` to initialize
4. Try commands like `/peso 70.5`, `/diario`, `/help`

## Troubleshooting

### Common Issues

**"No module named 'pytz'"**
```bash
pip install -r requirements.txt
```

**"Debes exportar TELEGRAM_TOKEN"**
```bash
export TELEGRAM_TOKEN="your_actual_token"
```

**Bot doesn't respond**
- Check if the bot is running (you should see "Bot started")
- Verify your token is correct
- Make sure you're messaging the right bot

**Permission denied errors**
```bash
chmod +x main.py
```

### Development Mode

For development with auto-restart:
```bash
# Install watchdog for auto-restart
pip install watchdog

# Run with auto-restart (optional)
watchmedo auto-restart --patterns="*.py" --recursive -- python main.py
```

## File Structure
```
weightlogs/
├── main.py           # Main entry point
├── config.py         # Configuration
├── database.py       # Database operations
├── handlers.py       # Command handlers
├── jobs.py          # Scheduled tasks
├── requirements.txt  # Dependencies
└── README.md        # Documentation
```

## Commands Available
- `/start` - Initialize bot
- `/help` - Show commands
- `/peso [kg]` - Record weight
- `/diario` - Last 6 days with chart
- `/semanal` - Last 4 weeks average
- `/mensual` - Last 6 months average 