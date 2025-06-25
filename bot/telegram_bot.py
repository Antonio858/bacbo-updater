# bot/telegram_bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pandas as pd
import os
from model.predictor import BacBoPredictor

predictor = BacBoPredictor()

# Cargar datos y entrenar modelo al iniciar
csv_path = os.path.join(os.path.dirname(__file__), "../data/bacbo_data.csv")
df = pd.read_csv(csv_path)
df["Resultado"] = df["Resultado"].str.strip().str.capitalize()
df["Resultado"] = df["Resultado"].replace({r"Tie \d+x": "Tie"}, regex=True)
df = df[df["Resultado"].isin(["Player", "Banker", "Tie"])]
X_train, X_val, y_train, y_val = predictor.preprocess_data(df)
predictor.train(X_train, y_train, X_val, y_val)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Soy el predictor de Bac Bo. Usa /prediccion para ver el próximo resultado.")

async def prediccion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ultimos = df["Resultado"].tolist()[-10:]
    if len(ultimos) == 10:
        pred = predictor.predict_next(ultimos)
        await update.message.reply_text(f"📊 Predicción para la próxima ronda: {pred}")
    else:
        await update.message.reply_text("No hay suficientes datos para predecir.")
