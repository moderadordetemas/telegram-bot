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

# Funcion para iniciar el servidor de Quart y el bot
async def run():
    loop = asyncio.get_event_loop()

    # Iniciar el bot
    await asyncio.gather(
        main(),  # Iniciar el bot
        app.run(host="0.0.0.0", port=3000)  # Iniciar el servidor Quart
    )

# Para evitar el error de event loop en Replit
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Iniciar el proceso
if __name__ == '__main__':
    loop.run_until_complete(run())