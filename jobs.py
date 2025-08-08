"""Scheduled jobs and automated tasks for the Telegram Weight Tracker Bot."""

import datetime as dt
import io
from typing import List, Tuple

import matplotlib.pyplot as plt
from telegram import InputFile, ForceReply
from telegram.ext import CallbackContext

from config import TZ
from database import get_weights

def is_first_day_of_month():
    today = dt.datetime.now(TZ).date()
    return today.day == 1

async def ask_weight_job(context: CallbackContext) -> None:
    uid = None
    # context.job.data may be dict, but the linter sees it as object
    data = getattr(getattr(context, "job", None), "data", None)
    if isinstance(data, dict):
        uid = data.get("user_id")
    if uid is None:
        print("[ERROR] Could not get user_id in ask_weight_job")
        return
    import datetime as dt
    today = dt.datetime.now().date()
    # Check if weight already registered for today
    weights_today = get_weights(uid, today, today)
    if weights_today:
        print(f"[DEBUG] User {uid} already registered weight for today, skipping reminder.")
        return
    print(f"[DEBUG] Sending daily reminder to {uid}")
    # Send message with ForceReply so it's auto-selected for reply
    message = await context.bot.send_message(
        uid,
        "Buenos días ☀️ ¿Cuál es tu peso de hoy?",
        reply_markup=ForceReply(selective=True)
    )
    # Store reminder message id to detect replies
    if context.bot_data is not None:
        context.bot_data.setdefault("reminder_messages", {})[uid] = message.message_id
    # Mark that weight is expected in chat_data
    if context.chat_data is not None:
        context.chat_data["expecting_daily_weight"] = True

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
    if not is_first_day_of_month():
        return
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

def register_jobs(app, user_id: int):
    if not hasattr(app, 'job_queue') or app.job_queue is None:
        print(f"[ERROR] Application has no job_queue! Scheduled jobs will not be registered for user {user_id}.")
        return
    # Remove previous jobs for this user
    for job in app.job_queue.get_jobs_by_name(str(user_id)):
        job.schedule_removal()
    for job in app.job_queue.get_jobs_by_name(f"weekly_{user_id}"):
        job.schedule_removal()
    for job in app.job_queue.get_jobs_by_name(f"monthly_{user_id}"):
        job.schedule_removal()

    # Daily weight question
    app.job_queue.run_daily(
        ask_weight_job,
        time=dt.time(hour=8, tzinfo=TZ),
        data={"user_id": user_id},
        name=str(user_id),
    )

    # Weekly summary (Monday 08:10)
    app.job_queue.run_daily(
        weekly_summary_job,
        time=dt.time(hour=8, minute=10, tzinfo=TZ),
        days=(0,),  # 0 = Monday
        data={"user_id": user_id},
        name=f"weekly_{user_id}",
    )

    # Monthly chart (1st day at 08:15)
    app.job_queue.run_daily(
        monthly_summary_job,
        time=dt.time(hour=8, minute=15, tzinfo=TZ),
        data={"user_id": user_id},
        name=f"monthly_{user_id}",
    ) 