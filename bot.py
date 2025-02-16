import logging
import asyncio
import threading
from quart import Quart
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token de tu bot (reemplaza con tu token real)
TOKEN = "7859944290:AAGq_vFC3JpdINiRZjnRKlYsx2T9n9Wk-uQ"

# Configurar la aplicación Quart
app = Quart(__name__)

@app.route("/")
async def index():
    return "Bot is running"

# Comando /start para el bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy tu bot.")

# Función asíncrona para iniciar el bot en el hilo principal
async def main_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    logger.info("✅ Bot iniciado correctamente.")
    # Ejecuta el polling en el hilo principal sin cerrar el event loop.
    await application.run_polling(close_loop=False)

# Función para iniciar el servidor Quart (bloqueante) en un hilo separado
def run_quart():
    # Nota: app.run() usa el servidor de desarrollo, ideal para pruebas en Replit.
    app.run(host="0.0.0.0", port=3000)

if __name__ == "__main__":
    # Iniciar el servidor Quart en un hilo separado (para mantener el entorno activo)
    quart_thread = threading.Thread(target=run_quart, daemon=True)
    quart_thread.start()

    # Ejecutar el bot en el hilo principal (así se permiten los manejadores de señales)
    asyncio.run(main_bot())