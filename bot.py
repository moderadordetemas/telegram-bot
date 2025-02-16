import asyncio
import nest_asyncio
nest_asyncio.apply()  # Permite "anidar" llamadas al event loop

import logging
from quart import Quart
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializa la aplicación Quart
app = Quart(__name__)

@app.route('/')
async def index():
    return "Bot is running"

# Función para manejar el comando /start en Telegram
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy tu bot de prueba.")

# Función asíncrona para iniciar el bot de Telegram
async def main_bot():
    application = Application.builder().token("7859944290:AAGq_vFC3JpdINiRZjnRKlYsx2T9n9Wk-uQ").build()
    application.add_handler(CommandHandler("start", start))
    logger.info("✅ Bot iniciado correctamente.")
    # Ejecuta el polling sin cerrar el event loop al finalizar
    await application.run_polling(close_loop=False)

# Función principal que ejecuta tanto el bot como el servidor web de Quart en paralelo
async def main():
    await asyncio.gather(
        main_bot(),
        app.run_task(host="0.0.0.0", port=3000)
    )

# Ejecutar todo en el hilo principal
if __name__ == '__main__':
    try:
        # Intenta obtener el event loop que ya esté corriendo
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Si no hay, crea uno nuevo
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.create_task(main())
    loop.run_forever()