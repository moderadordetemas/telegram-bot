import logging
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from quart import Quart

# Aplica nest_asyncio para permitir que se "aniden" llamadas al event loop
nest_asyncio.apply()

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configura la app de Quart (similar a Flask, pero asíncrona)
app = Quart(__name__)

@app.route('/')
async def index():
    return "Bot is running"

# Función para manejar el comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy tu bot de prueba.")

# Función que configura y ejecuta el bot de Telegram
async def main_bot():
    application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    application.add_handler(CommandHandler("start", start))
    logger.info("✅ Bot iniciado correctamente.")
    # Ejecuta el polling sin cerrar el event loop (close_loop=False)
    await application.run_polling(close_loop=False)

# Función que ejecuta en paralelo el bot y el servidor web de Quart
async def run_all():
    await asyncio.gather(
        main_bot(),
        app.run_task(host="0.0.0.0", port=10000)
    )

# Detecta si ya hay un event loop en ejecución
def run():
    try:
        # Intenta obtener el loop ya en ejecución (por ejemplo, en Replit)
        loop = asyncio.get_running_loop()
        loop.create_task(run_all())
    except RuntimeError:
        # Si no hay loop en ejecución, crea uno nuevo
        asyncio.run(run_all())

if __name__ == '__main__':
    run()