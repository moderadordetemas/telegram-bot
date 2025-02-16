import logging
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from quart import Quart

# Aplica nest_asyncio para permitir que se use asyncio.run() en un entorno con event loop activo.
nest_asyncio.apply()

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configura la aplicación Quart (similar a Flask, pero asíncrona)
app = Quart(__name__)

@app.route('/')
async def index():
    return "Bot is running"

# Función para manejar el comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy tu bot de prueba.")

# Función principal del bot
async def main():
    application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    application.add_handler(CommandHandler("start", start))
    logger.info("✅ Bot iniciado correctamente.")
    # Ejecuta el polling sin cerrar el event loop (close_loop=False)
    await application.run_polling(close_loop=False)

# Ejecuta el bot y el servidor web de Quart en paralelo
async def run_all():
    await asyncio.gather(
        main(),
        app.run_task(host="0.0.0.0", port=10000)
    )

if __name__ == '__main__':
    asyncio.run(run_all())