from telegram.ext import ApplicationBuilder
from telegram_bot import start, prediccion
from telegram.ext import CommandHandler
import os

TOKEN = os.getenv("8069988578:AAFFIp7Kem-HlNd2KivNpTvcnpFZxwMFpaA")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("prediccion", prediccion))

if __name__ == "__main__":
    print("Bot de Bac Bo iniciado...")
    app.run_polling()
