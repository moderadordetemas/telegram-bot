import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
from quart import Quart

# Configuración de logging
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

# Quart app (asíncrona, similar a Flask)
app = Quart(__name__)

# Ruta de ejemplo
@app.route('/')
async def index():
    return "Bot está corriendo"

# Función para iniciar el servidor y el bot
async def run_server_and_bot():
    # Ejecutar el bot en paralelo con el servidor Quart
    await asyncio.gather(
        main(),
        app.run_task(host="0.0.0.0", port=10000)  # Quart ejecutándose en paralelo
    )

# Ejecutar todo
if __name__ == "__main__":
    asyncio.run(run_server_and_bot())  # Ejecutar el servidor y el bot juntos