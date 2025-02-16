import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
from flask import Flask
from threading import Thread

# Configuración de logging para ver los mensajes del bot
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir la función para manejar el comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy tu bot de prueba.")

# Función principal del bot
async def main():
    # Inicia la aplicación del bot
    application = Application.builder().token("7859944290:AAGq_vFC3JpdINiRZjnRKlYsx2T9n9Wk-uQ").build()
    
    # Agregar el manejador de comandos
    application.add_handler(CommandHandler("start", start))
    
    # Iniciar el polling
    await application.run_polling()

# Flask app
app = Flask(__name__)

# Correr el bot en su hilo separado
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

# Correr Flask en su hilo separado
def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    # Hilos separados para Flask y el bot
    thread_flask = Thread(target=run_flask)
    thread_flask.start()
    
    thread_bot = Thread(target=run_bot)
    thread_bot.start()