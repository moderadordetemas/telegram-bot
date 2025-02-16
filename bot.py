import logging
import asyncio
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

# Función principal para iniciar el bot
async def start_bot():
    application = Application.builder().token(TOKEN).build()

    # Agregar comando /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Ejecutar el bot (utilizando el 'run_polling' para escuchar mensajes)
    await application.run_polling()

# Crear una función para iniciar tanto el servidor Quart como el bot
async def run():
    # Crear las tareas para ejecutar el bot y el servidor Quart en paralelo
    bot_task = asyncio.create_task(start_bot())
    web_task = asyncio.create_task(app.run_task(host="0.0.0.0", port=3000))

    # Esperar a que ambas tareas se completen (aunque no lo harán en este caso)
    await asyncio.gather(bot_task, web_task)

# Iniciar todo
if __name__ == '__main__':
    asyncio.run(run())