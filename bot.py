import logging
import asyncio
from threading import Thread
from quart import Quart
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token del bot (asegúrate de mantenerlo seguro en variables de entorno)
TOKEN = "TU_TOKEN_AQUI"

# Función de inicio
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("¡Hola! Soy tu bot de Telegram.")

# Función de manejo de mensajes
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

# Configuración de la aplicación de Telegram
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Función principal del bot
async def main():
    logger.info("Bot iniciado correctamente.")
    await application.run_polling()

# Iniciar el bot en el loop de eventos
loop = asyncio.get_event_loop()
loop.create_task(main())

# ---- Servidor Quart para mantener Replit activo ----
app = Quart(__name__)

@app.route('/')
async def home():
    return "¡Bot activo y en funcionamiento!"

def run():
    app.run(host="0.0.0.0", port=8080)

# Iniciar el servidor Quart en un hilo separado
Thread(target=run).start()