import logging
import asyncio
from quart import Quart
from telegram.ext import Application, CommandHandler
from telegram import Update
from telegram.ext import CallbackContext
from threading import Thread

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

# Función principal para iniciar el bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Agregar comando /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Ejecutar el bot (utilizando el 'run_polling' para escuchar mensajes)
    await application.run_polling()

# Funcion para iniciar el servidor de Quart y el bot
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

# Iniciar el bot en un hilo separado
bot_thread = Thread(target=run_bot)
bot_thread.start()

# Iniciar el servidor Quart
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)