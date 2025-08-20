STRINGS = {
    "start_message": (
        "¡Hola {first_name}!\n"
        "Cada día a las 08:00 te preguntaré tu peso.\n"
        "Puedes registrar cuando quieras usando /peso <kg> o solo /peso.\n"
        "Usa /diario para ver tus pesos con gráfico de evolución."
    ),
    "help_message": (
        "/peso [kg] – registra tu peso ahora (o pregunta si omites número)\n"
        "/mensual – media de los últimos 6 meses\n"
        "/semanal – media de las últimas 4 semanas\n"
        "/diario – pesos de los últimos 6 días + gráfico"
    ),
    "invalid_number": "Número no válido. Ejemplo: /peso 72.4",
    "weight_registered": "Peso registrado: {weight:.1f} kg ✅",
    "ask_weight_now": "¿Cuánto pesas ahora? Responde solo con el número.",
    "daily_reminder": "Buenos días ☀️ ¿Cuál es tu peso de hoy?",
    "diario_chart_caption": "📈 Gráfico de evolución de peso - Últimos 6 días",
    "mensual_chart_caption": "📈 Media mensual de peso - Últimos 6 meses",
    "semanal_chart_caption": "📈 Media semanal de peso - Últimas 4 semanas",
    "mensual_header": "📊 Media últimos 6 meses:",
    "semanal_header": "📅 Media últimas 4 semanas:",
    "diario_header": "📆 Pesos últimos 6 días:",
    "no_data": "sin datos",
    "unknown_command": "Lo siento, no entendí ese comando. Escribe /help para ver los comandos disponibles.",
    "reminders_off": "🔕 Recordatorios desactivados. No te enviaré el recordatorio matutino.",
    "reminders_on": "🔔 Recordatorios activados. Volveré a enviar el recordatorio matutino.",
    "weekly_summary_header": "Resumen semanal:",
    "weekly_summary_format": "Actual {current:.1f} kg vs. Anterior {previous:.1f} kg → {change}",
    "weekly_no_change": "↔️ Sin cambios (±0.0 kg)",
    "weekly_decrease": "⬇️ -{diff:.1f} kg",
    "weekly_increase": "⬆️ +{diff:.1f} kg",
    "monthly_chart_title": "Evolución peso – %B %Y",
    "monthly_summary_format": "{month}: inicio {start:.1f} kg / fin {end:.1f} kg\n{change}",
    "monthly_no_change": "↔️ Sin cambios este mes (±0.0 kg)",
    "monthly_decrease": "👏 Bajaste {diff:.1f} kg en el mes",
    "monthly_increase": "⚠️ Subiste {diff:.1f} kg en el mes",
} 