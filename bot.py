import logging
import asyncio
import threading
from quart import Quart
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import nest_asyncio

# Aplica nest_asyncio para permitir llamadas anidadas al event loop
nest_asyncio.apply()

# Inicializa la aplicación Quart (asíncrona)
app = Quart(__name__)

@app.route('/')
async def index():
    return "Bot is running"

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token de tu bot de Telegram (reemplaza con el tuyo)
TOKEN = '7859944290:AAGq_vFC3JpdINiRZjnRKlYsx2T9n9Wk-uQ'

# Comando /start del bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy tu bot de prueba.")

# Función para iniciar el bot de Telegram
def start_bot():
    # Crear un nuevo event loop para este hilo
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    logger.info("✅ Bot iniciado correctamente.")
    # Ejecutar el polling sin cerrar el event loop
    loop.run_until_complete(application.run_polling(close_loop=False))

# Función asíncrona para iniciar el servidor Quart
async def run_quart():
    await app.run_task(host="0.0.0.0", port=3000)

# Función para iniciar ambos procesos
def run_all():
    # Inicia el bot en un hilo separado
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    # Ejecuta el servidor Quart en el hilo principal usando asyncio.run
    asyncio.run(run_quart())

if __name__ == '__main__':
    run_all()