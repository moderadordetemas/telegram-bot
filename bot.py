import os
from telegram import Bot

# Obtener el token desde la variable de entorno
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Imprimir el token para verificar que se está leyendo correctamente
# print(f"Token obtenido: {TOKEN}")

# Crear instancia del bot
bot = Bot(token=TOKEN)