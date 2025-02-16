import logging
import asyncio
import nest_asyncio
from threading import Thread
from quart import Quart
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Aplica nest_asyncio para permitir llamadas anidadas al event loop
nest_asyncio.apply()

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializa la aplicación Quart (ASGI, asíncrona, similar a Flask)
app = Quart(__name__)

@app.route('/')
async def index():
    return "Bot is running"

# Definir el comando /start para el bot de Telegram
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy tu bot de prueba.")

# Función asíncrona para iniciar el bot de Telegram
async def main_bot():
    application = Application.builder().token("7859944290:AAGq_vFC3JpdINiRZjnRKlYsx2T9n9Wk-uQ").build()
    application.add_handler(CommandHandler("start", start))
    logger.info("✅ Bot iniciado correctamente.")
    # Ejecuta el polling sin cerrar el event loop y sin levantar señales (para evitar errores en hilos secundarios)
    await application.run_polling(close_loop=False, raise_signals=False)

# Función que se ejecuta en un hilo separado para el bot
def run_bot():
    # Crea un nuevo event loop para este hilo
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_bot())

# Función asíncrona para iniciar el servidor Quart en el hilo principal
async def main_quart():
    await app.run_task(host="0.0.0.0", port=3000)

# Función para iniciar ambos procesos en paralelo
def run_all():
    # Inicia el bot en un hilo separado
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    # Inicia el servidor Quart en el hilo principal usando asyncio.run
    asyncio.run(main_quart())

if __name__ == '__main__':
    run_all()