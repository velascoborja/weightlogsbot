"""Command and message handlers for the Telegram Weight Tracker Bot."""

import datetime as dt
import io
from typing import List, Tuple

import matplotlib.pyplot as plt
from telegram import InputFile, Update
from telegram.ext import CallbackContext

from config import TZ
from database import save_weight, get_monthly_weights, get_weekly_weights, get_daily_weights, get_weights


async def start(update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hola {user.first_name}!\n"
        "Cada día a las 08:00 te preguntaré tu peso.\n"
        "Puedes registrar cuando quieras usando /peso <kg> o /peso sin número.\n"
        "Usa /diario para ver tus pesos con gráfico de evolución."
    )


async def help_cmd(update: Update, context: CallbackContext) -> None:
    """Handle the /help command."""
    await update.message.reply_text(
        "/peso [kg] – registra tu peso ahora (o pregunta si omites número)\n"
        "/mensual – media de los últimos 6 meses\n"
        "/semanal – media de las últimas 4 semanas\n"
        "/diario – pesos de los últimos 6 días + gráfico"
    )


async def _register_weight_arg(update: Update, context: CallbackContext, arg: str) -> None:
    """Register weight from command argument or user input."""
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
    """Handle the /peso command."""
    # Si viene número, registrar directamente
    if context.args:
        await _register_weight_arg(update, context, context.args[0])
    else:
        # Preguntar y esperar respuesta
        await update.message.reply_text("¿Cuánto pesas ahora? Responde solo con el número.")
        context.user_data["awaiting_weight"] = True


async def numeric_listener(update: Update, context: CallbackContext) -> None:
    """Handle numeric input from users."""
    text = update.message.text.strip()
    if not text.replace(",", ".").replace(".", "", 1).isdigit():
        return
    
    # Guardamos solo si se esperaba un número o aceptamos números espontáneos
    if not context.user_data.get("awaiting_weight") and not context.chat_data.get("expecting_daily_weight", False):
        return
    
    await _register_weight_arg(update, context, text)


async def mensual_cmd(update: Update, context: CallbackContext) -> None:
    """Handle the /mensual command."""
    user_id = update.effective_user.id
    monthly_data = get_monthly_weights(user_id)
    
    lines = ["📊 Media últimos 6 meses:"]
    for month_name, avg_weight in monthly_data:
        weight_text = f"{avg_weight:.1f} kg" if avg_weight is not None else "sin datos"
        lines.append(f"{month_name}: {weight_text}")
    
    await update.message.reply_text("\n".join(lines))


async def semanal_cmd(update: Update, context: CallbackContext) -> None:
    """Handle the /semanal command."""
    user_id = update.effective_user.id
    weekly_data = get_weekly_weights(user_id)
    
    lines = ["📅 Media últimas 4 semanas:"]
    for span, avg_weight in weekly_data:
        weight_text = f"{avg_weight:.1f} kg" if avg_weight is not None else "sin datos"
        lines.append(f"{span}: {weight_text}")
    
    await update.message.reply_text("\n".join(lines))


async def diario_cmd(update: Update, context: CallbackContext) -> None:
    """Handle the /diario command."""
    user_id = update.effective_user.id
    today = dt.datetime.now(TZ).date()
    
    # Get data for the last 6 days
    start_date = today - dt.timedelta(days=5)
    weights_data = get_weights(user_id, start_date, today)
    
    # Prepare text response
    lines = ["📆 Pesos últimos 6 días:"]
    for i in range(6):
        d = today - dt.timedelta(days=i)
        ws = get_weights(user_id, d, d)
        weight_text = f"{ws[-1][1]:.1f} kg" if ws else "sin datos"
        lines.append(f"{d.strftime('%d/%m')}: {weight_text}")
    
    # Send text first
    await update.message.reply_text("\n".join(lines))
    
    # Create and send chart if we have data
    if len(weights_data) >= 2:
        dates = [d for d, _ in weights_data]
        vals = [w for _, w in weights_data]
        
        # Create chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, vals, marker="o", linewidth=2, markersize=6)
        ax.set_title("Evolución peso - Últimos 6 días", fontsize=14, fontweight='bold')
        ax.set_ylabel("Kg", fontsize=12)
        ax.set_xlabel("Fecha", fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on points
        for i, (date, weight) in enumerate(zip(dates, vals)):
            ax.annotate(f'{weight:.1f}', (date, weight), 
                       textcoords="offset points", xytext=(0,10), 
                       ha='center', fontsize=10)
        
        plt.tight_layout()
        
        # Save to buffer
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        
        # Send chart
        await update.message.reply_photo(
            InputFile(buf, "peso_diario.png"),
            caption="📈 Gráfico de evolución de peso - Últimos 6 días"
        ) 