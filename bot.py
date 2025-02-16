import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
from flask import Flask

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

# Route para mostrar algo en la página
@app.route('/')
def index():
    return "Bot está corriendo"

if __name__ == "__main__":
    # Iniciar Flask y el bot en el hilo principal
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())  # Ejecutar el bot
    app.run(host="0.0.0.0", port=10000)  # Ejecutar Flask