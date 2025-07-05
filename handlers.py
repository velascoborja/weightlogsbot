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
    print("[DEBUG] Entrando a diario_cmd")
    user_id = update.effective_user.id
    today = dt.datetime.now(TZ).date()
    print(f"[DEBUG] user_id: {user_id}, today: {today}")
    
    # Get data for the last 6 days
    start_date = today - dt.timedelta(days=5)
    print(f"[DEBUG] start_date: {start_date}")
    weights_data = get_weights(user_id, start_date, today)
    print(f"[DEBUG] weights_data: {weights_data}")
    
    # Prepare text response
    lines = ["📆 Pesos últimos 6 días:"]
    for i in range(6):
        d = today - dt.timedelta(days=i)
        ws = get_weights(user_id, d, d)
        print(f"[DEBUG] Día: {d}, ws: {ws}")
        weight_text = f"{ws[0][1]:.1f} kg" if ws else "sin datos"
        lines.append(f"{d.strftime('%d/%m')}: {weight_text}")
    
    print(f"[DEBUG] lines: {lines}")
    # Send text first
    try:
        await update.message.reply_text("\n".join(lines))
        print("[DEBUG] Mensaje de texto enviado")
    except Exception as e:
        print(f"[ERROR] Error enviando mensaje de texto: {e}")
    
    # Create and send chart if we have data
    if len(weights_data) >= 2:
        print("[DEBUG] Hay suficientes datos para el gráfico")
        dates = [d for d, _ in weights_data]
        vals = [w for _, w in weights_data]
        try:
            # Create chart
            fig, ax = plt.subplots(figsize=(10, 6))
            # Convert dates to matplotlib dates for plotting
            import matplotlib.dates as mdates
            dates_mpl = [mdates.date2num(d) for d in dates]
            ax.plot(dates_mpl, vals, marker="o", linewidth=2, markersize=6)
            ax.set_title("Evolución peso - Últimos 6 días", fontsize=14, fontweight='bold')
            ax.set_ylabel("Kg", fontsize=12)
            ax.set_xlabel("Fecha", fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='x', rotation=45)
            
            # Format x-axis to show dates properly
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            ax.xaxis.set_major_locator(mdates.DayLocator())
            
            for i, (date, weight) in enumerate(zip(dates_mpl, vals)):
                ax.annotate(f'{weight:.1f}', (date, weight), 
                           textcoords="offset points", xytext=(0,10), 
                           ha='center', fontsize=10)
            plt.tight_layout()
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=150, bbox_inches='tight')
            plt.close(fig)
            buf.seek(0)
            print("[DEBUG] Gráfico generado correctamente")
            await update.message.reply_photo(
                InputFile(buf, "peso_diario.png"),
                caption="📈 Gráfico de evolución de peso - Últimos 6 días"
            )
            print("[DEBUG] Foto enviada correctamente")
        except Exception as e:
            print(f"[ERROR] Error generando o enviando el gráfico: {e}")
    else:
        print("[DEBUG] No hay suficientes datos para enviar gráfico") 