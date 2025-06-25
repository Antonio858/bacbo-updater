# test_scraping.py
from historicbet_scraper import fetch_data_from_historicbet

def test_scraping():
    df = fetch_data_from_historicbet()
    if df.empty:
        print("⚠️ No se extrajeron datos. Verifica el selector o el contenido de la página.")
    else:
        print("✅ Datos extraídos correctamente:")
        print(df.head())

if __name__ == "__main__":
    test_scraping()
