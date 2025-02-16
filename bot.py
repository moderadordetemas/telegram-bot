import logging
import asyncio
import threading
from quart import Quart
from telegram.ext import Application, CommandHandler
from telegram import Update
from telegram.ext import CallbackContext

# Inicialización de la aplicación Quart
app = Quart(__name__)

# Configuración de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token de tu bot de Telegram
TOKEN = '7859944290:AAGq_vFC3JpdINiRZjnRKlYsx2T9n9Wk-uQ'

# Comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply("¡Hola! Soy tu bot.")

# Ruta para la raíz
@app.route('/')
async def index():
    return 'Servidor en ejecución'

# Función para iniciar el bot
def start_bot():
    # Crear un bucle de eventos en este hilo
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    application = Application.builder().token(TOKEN).build()

    # Agregar comando /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Ejecutar el bot (utilizando el 'run_polling' para escuchar mensajes)
    loop.run_until_complete(application.run_polling())

# Función principal para iniciar el servidor Quart y el bot en paralelo
async def run():
    # Crear tarea para el servidor web
    web_task = asyncio.create_task(app.run_task(host="0.0.0.0", port=3000))

    # Iniciar el bot en un hilo separado
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    # Esperar a que el servidor web esté activo (esta tarea nunca termina)
    await web_task

# Iniciar todo
if __name__ == '__main__':
    asyncio.run(run())