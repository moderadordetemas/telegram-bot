import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"
    
# Cargar el token desde las variables de entorno
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Lista de palabras prohibidas (puedes personalizarla)
PROHIBITED_WORDS = ["palabra1", "palabra2", "insulto", "spam"]

# ID de los temas donde se aplicará el filtro (reemplaza con los reales)
TOPIC_IDS = [123456789, 987654321]  # IDs de los temas específicos

def delete_prohibited_message(update: Update, context: CallbackContext):
    """Elimina mensajes con palabras prohibidas y advierte al usuario."""
    message = update.message
    chat_id = message.chat_id
    topic_id = message.message_thread_id  # Obtiene el ID del tema en el grupo

    if topic_id in TOPIC_IDS:  # Solo actúa en temas específicos
        for word in PROHIBITED_WORDS:
            if word.lower() in message.text.lower():
                try:
                    # Borrar el mensaje
                    context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                    
                    # Enviar advertencia al usuario
                    warning_text = f"⚠️ @{message.from_user.username}, tu mensaje fue eliminado por contener palabras no permitidas."
                    context.bot.send_message(chat_id=chat_id, text=warning_text, message_thread_id=topic_id)
                except Exception as e:
                    print(f"Error al eliminar mensaje: {e}")
                break  # Salir del bucle si encuentra una palabra prohibida

def start(update: Update, context: CallbackContext):
    """Mensaje de bienvenida cuando el bot inicia."""
    update.message.reply_text("👋 ¡Hola! Estoy activo y moderando mensajes en este grupo.")

def main():
    """Configura el bot y lo mantiene ejecutándose."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Comando /start
    dp.add_handler(CommandHandler("start", start))

    # Manejo de mensajes para filtrar palabras prohibidas
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, delete_prohibited_message))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

def get_topic_id(update: Update, context: CallbackContext):
    """Responde con el ID del tema cuando alguien escribe /getid en un tema."""
    topic_id = update.message.message_thread_id
    chat_id = update.message.chat_id
    
    update.message.reply_text(f"📌 Chat ID: {chat_id}\n🆔 Topic ID: {topic_id}")

# Agregar el comando al bot
dp.add_handler(CommandHandler("getid", get_topic_id))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)