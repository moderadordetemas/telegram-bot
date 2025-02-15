from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
import logging
import asyncio
import threading

# Configura Flask
app = Flask(__name__)

# Esta es la función para responder al comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! El bot está funcionando.")

# Configura la aplicación de Telegram
async def main():
    # Obtén tu token de Bot de Telegram
    application = Application.builder().token("7859944290:AAGq_vFC3JpdINiRZjnRKlYsx2T9n9Wk-uQ").build()

    # Registra el manejador para el comando /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Inicia el bot
    await application.run_polling()

# Función para ejecutar el bot
def run_bot():
    # Crea la tarea asíncrona sin bloquear el hilo
    asyncio.create_task(main())

# Ruta simple para que Flask mantenga la aplicación web viva
@app.route('/')
def index():
    return "El bot está corriendo."

# Inicia Flask en un hilo separado
def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == '__main__':
    # Crea un hilo para ejecutar Flask
    threading.Thread(target=run_flask).start()

    # Ejecuta el bot en el hilo principal
    run_bot()
