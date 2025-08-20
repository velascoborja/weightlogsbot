STRINGS = {
    "start_message": (
        "Hello {first_name}!\n"
        "Every day at 08:00 I will ask you your weight.\n"
        "You can log it anytime using /peso <kg> or just /peso.\n"
        "Use /diario to see your weights with an evolution chart."
    ),
    "help_message": (
        "/peso [kg] – log your weight now (or I will ask if you omit the number)\n"
        "/mensual – average of the last 6 months\n"
        "/semanal – average of the last 4 weeks\n"
        "/diario – weights of the last 6 days + chart"
    ),
    "invalid_number": "Invalid number. Example: /peso 72.4",
    "weight_registered": "Weight registered: {weight:.1f} kg ✅",
    "ask_weight_now": "How much do you weigh now? Reply with just the number.",
    "daily_reminder": "Good morning ☀️ What's your weight today?",
    "diario_chart_caption": "📈 Weight evolution chart - Last 6 days",
    "mensual_chart_caption": "📈 Monthly average weight - Last 6 months",
    "semanal_chart_caption": "📈 Weekly average weight - Last 4 weeks",
    "mensual_header": "📊 Average of the last 6 months:",
    "semanal_header": "📅 Average of the last 4 weeks:",
    "diario_header": "📆 Weights for the last 6 days:",
    "no_data": "no data",
    "unknown_command": "Sorry, I didn't understand that command. Type /help to see available commands.",
    "reminders_off": "🔕 Reminders disabled. I won't send the morning reminder.",
    "reminders_on": "🔔 Reminders enabled. I'll resume the morning reminder.",
    "weekly_summary_header": "Weekly summary:",
    "weekly_summary_format": "Current {current:.1f} kg vs. Previous {previous:.1f} kg → {change}",
    "weekly_no_change": "↔️ No change (±0.0 kg)",
    "weekly_decrease": "⬇️ -{diff:.1f} kg",
    "weekly_increase": "⬆️ +{diff:.1f} kg",
    "monthly_chart_title": "Weight evolution – %B %Y",
    "monthly_summary_format": "{month}: start {start:.1f} kg / end {end:.1f} kg\n{change}",
    "monthly_no_change": "↔️ No change this month (±0.0 kg)",
    "monthly_decrease": "👏 You lost {diff:.1f} kg this month",
    "monthly_increase": "⚠️ You gained {diff:.1f} kg this month",
} 