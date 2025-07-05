# Telegram Weight Tracker Bot

A Telegram bot that tracks daily weight, sends weekly summaries, and monthly reports with charts.

## Features

- **Daily weight tracking**: Record your weight with `/peso <kg>` or just `/peso` to be prompted
- **Weekly summaries**: Automatic comparison of current vs previous week averages
- **Monthly reports**: Charts showing weight evolution over the month
- **On-demand reports**: Get daily, weekly, or monthly summaries anytime
- **Visual charts**: Daily weight evolution charts with the `/diario` command
- **Automatic reminders**: Daily prompts at 8:00 AM

## Commands

- `/start` - Initialize the bot and get welcome message
- `/help` - Show available commands
- `/peso [kg]` - Record your weight (prompts if no number provided)
- `/diario` - Show weights for the last 6 days with evolution chart
- `/semanal` - Show averages for the last 4 weeks
- `/mensual` - Show averages for the last 6 months

## Project Structure

```
weightlogs/
├── config.py          # Configuration settings and environment variables
├── database.py        # Database operations and weight data management
├── handlers.py        # Command and message handlers
├── jobs.py           # Scheduled tasks and automated messages
├── main.py           # Main application entry point
├── requirements.txt  # Python dependencies
├── Procfile         # Heroku deployment configuration
└── README.md        # This file
```

## Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd weightlogs
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Telegram bot**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot with `/newbot`
   - Copy the token provided

5. **Configure environment variables**
   ```bash
   export TELEGRAM_TOKEN="your_bot_token_here"
   export BOT_TZ="Europe/Madrid"  # Optional: your timezone
   export WEIGHT_DB="weights.db"  # Optional: custom database file
   ```

6. **Run the bot**
   ```bash
   python main.py
   ```

## Configuration

### Environment Variables

- `TELEGRAM_TOKEN` (required): Your bot token from BotFather
- `BOT_TZ` (optional): Timezone for scheduling (default: Europe/Madrid)
- `WEIGHT_DB` (optional): Database file path (default: weights.db)

### Scheduled Jobs

The bot automatically schedules these jobs for each user:

- **Daily weight question**: 8:00 AM every day
- **Weekly summary**: Monday 8:10 AM
- **Monthly chart**: 1st day of month at 8:15 AM

## Database

The bot uses SQLite to store weight data with the following schema:

```sql
CREATE TABLE weights (
    user_id INTEGER,
    date TEXT,
    weight REAL,
    PRIMARY KEY (user_id, date)
);
```

## Deployment

### Heroku

The project includes a `Procfile` for easy Heroku deployment:

1. Create a new Heroku app
2. Set environment variables in Heroku dashboard
3. Deploy using Git or Heroku CLI

### Other Platforms

The bot can be deployed on any platform that supports Python:
- Railway
- Render
- DigitalOcean App Platform
- AWS Lambda (with modifications)

## Development

### Adding New Commands

1. Add the handler function in `handlers.py`
2. Import and register the handler in `main.py`

### Adding New Jobs

1. Add the job function in `jobs.py`
2. Register the job in the `register_jobs` function

### Database Operations

All database operations are centralized in `database.py` for easy maintenance and testing.

## License

This project is open source. Feel free to modify and distribute as needed. 