from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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

if __name__ == '__main__':
    # Solo llama a la función main sin asyncio.run()
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Agrega el task al event loop existente
    loop.run_forever()  # Ejecuta el loop indefinidamente