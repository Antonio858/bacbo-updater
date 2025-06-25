import time
from historicbet_scraper import fetch_data_from_historicbet

if __name__ == "__main__":
    print("⏳ Iniciando actualización automática de datos de Bac Bo...")
    while True:
        try:
            df = fetch_data_from_historicbet()
            print(f"✅ Datos actualizados. Última ronda: {df.iloc[0].to_dict()}")
        except Exception as e:
            print(f"❌ Error durante la actualización: {e}")
        time.sleep(300)  # Espera 5 minutos
