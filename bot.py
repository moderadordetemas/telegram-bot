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

# Función principal para iniciar el bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Agregar comando /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Ejecutar el bot (utilizando el 'run_polling' para escuchar mensajes)
    await application.run_polling()

# Crear una función para iniciar tanto el servidor Quart como el bot
async def run():
    # Iniciar el bot
    bot_task = asyncio.create_task(main())
    
    # Iniciar el servidor Quart
    await app.run_task(host="0.0.0.0", port=3000)

    # Esperar a que el bot termine su ejecución (aunque no lo hará)
    await bot_task

# Iniciar todo
if __name__ == '__main__':
    asyncio.run(run())