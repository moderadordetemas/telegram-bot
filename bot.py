import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configurar Flask para mantener el bot en ejecución
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

# Cargar el token desde las variables de entorno
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Lista de palabras prohibidas (puedes personalizarla)
PROHIBITED_WORDS = ["palabra1", "palabra2", "insulto", "spam"]

# ID de los temas donde se aplicará el filtro (reemplaza con los reales)
TOPIC_IDS = [2,5]  # IDs de los temas específicos

# Función que eliminará el mensaje si contiene palabras prohibidas
async def delete_prohibited_message(update: Update, context: CallbackContext):
    """Elimina mensajes con palabras prohibidas y advierte al usuario."""
    message = update.message
    chat_id = message.chat_id
    topic_id = message.message_thread_id  # Obtiene el ID del tema en el grupo

    if topic_id in TOPIC_IDS:  # Solo actúa en temas específicos
        for word in PROHIBITED_WORDS:
            if word.lower() in message.text.lower():
                try:
                    # Borrar el mensaje
                    await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                    
                    # Enviar advertencia al usuario
                    warning_text = f"⚠️ @{message.from_user.username}, tu mensaje fue eliminado por contener palabras no permitidas."
                    await context.bot.send_message(chat_id=chat_id, text=warning_text, message_thread_id=topic_id)
                except Exception as e:
                    print(f"Error al eliminar mensaje: {e}")
                break  # Salir del bucle si encuentra una palabra prohibida

# Función que responde con el ID del tema cuando se usa el comando /getid
async def get_topic_id(update: Update, context: CallbackContext):
    """Responde con el ID del tema cuando alguien escribe /getid en un tema."""
    topic_id = update.message.message_thread_id
    chat_id = update.message.chat_id
    
    await update.message.reply_text(f"📌 Chat ID: {chat_id}\n🆔 Topic ID: {topic_id}")

# Función de inicio, muestra un mensaje de bienvenida
async def start(update: Update, context: CallbackContext):
    """Mensaje de bienvenida cuando el bot inicia."""
    await update.message.reply_text("👋 ¡Hola! Estoy activo y moderando mensajes en este grupo.")

# Configura el bot y lo mantiene ejecutándose
async def main():
    """Configura el bot y lo mantiene ejecutándose."""
    # Crea la aplicación del bot con el token
    application = Application.builder().token(TOKEN).build()

    # Comandos del bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getid", get_topic_id))

    # Manejo de mensajes para filtrar palabras prohibidas
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_prohibited_message))

    print("✅ Bot iniciado correctamente.")
    
    # Ejecutar el bot en un hilo separado
    await application.run_polling()

# Ejecutar Flask y el bot en paralelo
def run():
    loop = asyncio.get_event_loop()
    
    # Ejecutar el bot en segundo plano
    asyncio.create_task(main())
    
    # Ejecutar Flask en el hilo principal
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    run()