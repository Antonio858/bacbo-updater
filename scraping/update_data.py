# update_data.py
import time
import os
import pandas as pd
import subprocess
from historicbet_scraper import fetch_data_from_historicbet
from model.predictor import BacBoPredictor

GIT_USERNAME = os.getenv("GIT_USERNAME")
GIT_EMAIL = os.getenv("GIT_EMAIL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REPO_URL = f"https://{GIT_USERNAME}:{GITHUB_TOKEN}@github.com/{GIT_USERNAME}/bacbo-updater.git"

if __name__ == "__main__":
    print("⏳ Iniciando actualización automática de datos de Bac Bo...")
    while True:
        try:
            df = fetch_data_from_historicbet()
            print(f"✅ Datos actualizados. Última ronda: {df.iloc[0].to_dict()}")

            predictor = BacBoPredictor()
            df["Resultado"] = df["Resultado"].str.strip().str.capitalize()
            df["Resultado"] = df["Resultado"].replace({r"Tie \d+x": "Tie"}, regex=True)
            df = df[df["Resultado"].isin(["Player", "Banker", "Tie"])]

            X_train, X_val, y_train, y_val = predictor.preprocess_data(df)
            predictor.train(X_train, y_train, X_val, y_val)

            ultimos = df["Resultado"].tolist()[-10:]
            if len(ultimos) == 10:
                pred = predictor.predict_next(ultimos)
                print(f"🎯 Predicción guardada: {pred}")

                os.makedirs("data", exist_ok=True)
                pred_path = "data/ultima_prediccion.csv"
                pd.DataFrame([[pred]], columns=["Prediccion"]).to_csv(pred_path, index=False)

                # Subir a GitHub
                subprocess.run(["git", "config", "--global", "user.name", GIT_USERNAME])
                subprocess.run(["git", "config", "--global", "user.email", GIT_EMAIL])
                subprocess.run(["git", "add", pred_path])
                subprocess.run(["git", "commit", "-m", f"Actualización automática: {pred}"], check=False)
                subprocess.run(["git", "push", REPO_URL, "main"], check=False)

        except Exception as e:
            print(f"❌ Error durante la actualización: {e}")

        time.sleep(10)  # Espera 10 segundos
