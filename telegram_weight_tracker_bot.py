# telegram_weight_tracker_bot.py
"""Telegram bot que registra tu peso diario, envía resúmenes semanales y un informe
mensual con gráfico de evolución. Ahora incluye:

  • /peso [<kg>]  → registra peso (si omites número, pregunta y espera)
  • /mensual      → promedios de los últimos 6 meses
  • /semanal      → promedios de las últimas 4 semanas
  • /diario       → pesos de los últimos 6 días

Instalación rápida (virtualenv recomendado):
    python -m venv .venv && source .venv/bin/activate
    pip install "python-telegram-bot[rate-limiter]==21.1" matplotlib pytz

Después:
    export TELEGRAM_TOKEN="<TU_TOKEN>"
    python telegram_weight_tracker_bot.py
"""

from __future__ import annotations

import datetime as dt
import io
import os
import sqlite3
from contextlib import closing
from typing import List, Tuple

import matplotlib.pyplot as plt
import pytz
from telegram import InputFile, Update
from telegram.ext import (
    AIORateLimiter,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)

# ------------------------- Configuración ---------------------------------------------------------
DB_FILE = os.getenv("WEIGHT_DB", "weights.db")
TOKEN = os.getenv("TELEGRAM_TOKEN")
TZ = pytz.timezone(os.getenv("BOT_TZ", "Europe/Madrid"))
DAILY_HOUR = 8  # 08:00

# ------------------------- Base de datos ---------------------------------------------------------

def init_db() -> None:
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
    with closing(sqlite3.connect(DB_FILE)) as conn:
        conn.execute(
            "REPLACE INTO weights (user_id, date, weight) VALUES (?,?,?)",
            (user_id, date.isoformat(), weight),
        )
        conn.commit()


def get_weights(user_id: int, start: dt.date, end: dt.date) -> List[Tuple[dt.date, float]]:
    with closing(sqlite3.connect(DB_FILE)) as conn:
        cur = conn.execute(
            "SELECT date, weight FROM weights WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date",
            (user_id, start.isoformat(), end.isoformat()),
        )
        rows = cur.fetchall()
    return [(dt.date.fromisoformat(d), w) for d, w in rows]

# ------------------------- Comandos básicos ------------------------------------------------------

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Hola {user.first_name}!\n"
        "Cada día a las 08:00 te preguntaré tu peso.\n"
        "Puedes registrar cuando quieras usando /peso <kg> o /peso sin número."
    )

async def help_cmd(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "/peso [kg] – registra tu peso ahora (o pregunta si omites número)\n"
        "/mensual – media de los últimos 6 meses\n"
        "/semanal – media de las últimas 4 semanas\n"
        "/diario – pesos de los últimos 6 días"
    )

# ------------------------- Registro de peso ------------------------------------------------------

async def _register_weight_arg(update: Update, context: CallbackContext, arg: str) -> None:
    try:
        weight = float(arg.replace(",", "."))
    except ValueError:
        await update.message.reply_text("Número no válido. Ejemplo: /peso 72.4")
        return
    user_id = update.effective_user.id
    today = dt.datetime.now(TZ).date()
    save_weight(user_id, today, weight)
    context.user_data["awaiting_weight"] = False
    await update.message.reply_text(f"Peso registrado: {weight:.1f} kg ✅")

async def peso_cmd(update: Update, context: CallbackContext) -> None:
    # Si viene número, registrar directamente
    if context.args:
        await _register_weight_arg(update, context, context.args[0])
    else:
        # Preguntar y esperar respuesta
        await update.message.reply_text("¿Cuánto pesas ahora? Responde solo con el número.")
        context.user_data["awaiting_weight"] = True

async def numeric_listener(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip()
    if not text.replace(",", ".").replace(".", "", 1).isdigit():
        return
    # Guardamos solo si se esperaba un número o aceptamos números espontáneos
    if not context.user_data.get("awaiting_weight") and not context.chat_data.get("expecting_daily_weight", False):
        return
    await _register_weight_arg(update, context, text)

# ------------------------- Informes bajo demanda -------------------------------------------------

def _month_end(date_: dt.date) -> dt.date:
    next_month = date_.replace(day=28) + dt.timedelta(days=4)
    return next_month.replace(day=1) - dt.timedelta(days=1)

async def mensual_cmd(update: Update, context: CallbackContext) -> None:
    today = dt.datetime.now(TZ).date()
    user_id = update.effective_user.id
    lines = ["📊 Media últimos 6 meses:"]
    for offset in range(0, 6):
        tot = today.year * 12 + today.month - 1 - offset
        year, month = divmod(tot, 12)
        month += 1
        start = dt.date(year, month, 1)
        end = _month_end(start)
        ws = get_weights(user_id, start, end)
        lines.append(
            f"{start.strftime('%b %Y')}: " + (f"{sum(w for _, w in ws)/len(ws):.1f} kg" if ws else "sin datos")
        )
    await update.message.reply_text("\n".join(lines))

async def semanal_cmd(update: Update, context: CallbackContext) -> None:
    today = dt.datetime.now(TZ).date()
    user_id = update.effective_user.id
    monday = today - dt.timedelta(days=today.weekday())
    lines = ["📅 Media últimas 4 semanas:"]
    for i in range(0, 4):
        start = monday - dt.timedelta(days=7 * i)
        end = start + dt.timedelta(days=6)
        ws = get_weights(user_id, start, end)
        span = f"{start.strftime('%d/%m')}–{end.strftime('%d/%m')}"
        lines.append(span + ": " + (f"{sum(w for _, w in ws)/len(ws):.1f} kg" if ws else "sin datos"))
    await update.message.reply_text("\n".join(lines))

async def diario_cmd(update: Update, context: CallbackContext) -> None:
    today = dt.datetime.now(TZ).date()
    user_id = update.effective_user.id
    lines = ["📆 Pesos últimos 6 días:"]
    for i in range(0, 6):
        d = today - dt.timedelta(days=i)
        ws = get_weights(user_id, d, d)
        lines.append(
            f"{d.strftime('%d/%m')}: " + (f"{ws[-1][1]:.1f} kg" if ws else "sin datos")
        )
    await update.message.reply_text("\n".join(lines))

# ------------------------- Jobs automáticos ------------------------------------------------------

async def ask_weight_job(context: CallbackContext) -> None:
    uid = context.job.data["user_id"]
    await context.bot.send_message(uid, "Buenos días ☀️ ¿Cuál es tu peso de hoy?")

async def weekly_summary_job(context: CallbackContext) -> None:
    uid = context.job.data["user_id"]
    today = dt.datetime.now(TZ).date()
    this_start = today - dt.timedelta(days=today.weekday())
    last_start = this_start - dt.timedelta(days=7)
    this_ws = get_weights(uid, this_start, today)
    last_ws = get_weights(uid, last_start, this_start - dt.timedelta(days=1))
    if len(this_ws) < 2 or len(last_ws) < 2:
        return
    avg_this = sum(w for _, w in this_ws) / len(this_ws)
    avg_last = sum(w for _, w in last_ws) / len(last_ws)
    diff = avg_this - avg_last
    await context.bot.send_message(
        uid,
        f"Resumen semanal:\nActual {avg_this:.1f} kg vs. Anterior {avg_last:.1f} kg → "
        f"{'⬇️ -' if diff<0 else '⬆️ +'}{abs(diff):.1f} kg",
    )

async def monthly_summary_job(context: CallbackContext) -> None:
    uid = context.job.data["user_id"]
    today = dt.datetime.now(TZ).date()
    last_month_end = today.replace(day=1) - dt.timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    ws = get_weights(uid, last_month_start, last_month_end)
    if len(ws) < 2:
        return
    dates = [d for d, _ in ws]
    vals = [w for _, w in ws]
    fig, ax = plt.subplots()
    ax.plot(dates, vals, marker="o")
    ax.set_title(last_month_start.strftime("Evolución peso – %B %Y"))
    ax.set_ylabel("Kg")
    ax.grid(True)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    diff = vals[-1] - vals[0]
    caption = (
        f"{last_month_start.strftime('%b %Y')}: inicio {vals[0]:.1f} kg / fin {vals[-1]:.1f} kg\n"
        f"{'👏 Bajaste' if diff<0 else '⚠️ Subiste'} {abs(diff):.1f} kg en el mes"
    )
    await context.bot.send_photo(uid, InputFile(buf, "peso.png"), caption=caption)

# ------------------------- Programación de jobs --------------------------------------------------

async def register_jobs(app, user_id: int):
    # Elimina jobs previos de ese usuario
    for job in app.job_queue.get_jobs_by_name(str(user_id)):
        job.schedule_removal()

    # Pregunta diaria
    app.job_queue.run_daily(
        ask_weight_job,
        time=dt.time(hour=DAILY_HOUR, tzinfo=TZ),
        data={"user_id": user_id},
        name=str(user_id),
    )

    # Resumen semanal (lunes 08:10)
    app.job_queue.run_weekly(
        weekly_summary_job,
        time=dt.time(hour=DAILY_HOUR, minute=10, tzinfo=TZ),
        day_of_week=0,
        data={"user_id": user_id},
        name=str(user_id),
    )

    # Gráfico mensual (día 1 a las 08:15)
    app.job_queue.run_monthly(
        monthly_summary_job,
        time=dt.time(hour=DAILY_HOUR, minute=15, tzinfo=TZ),
        day=1,
        data={"user_id": user_id},
        name=str(user_id),
    )

# ------------------------- Main ------------------------------------------------------------------

def main() -> None:
    if not TOKEN:
        raise RuntimeError("Debes exportar TELEGRAM_TOKEN con tu token de BotFather")

    init_db()

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .rate_limiter(AIORateLimiter())
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("peso", peso_cmd))
    app.add_handler(CommandHandler("mensual", mensual_cmd))
    app.add_handler(CommandHandler("semanal", semanal_cmd))
    app.add_handler(CommandHandler("diario", diario_cmd))

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), numeric_listener))

    app.run_polling()


if __name__ == "__main__":
    main()
