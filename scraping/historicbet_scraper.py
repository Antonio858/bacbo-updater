import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def fetch_data_from_historicbet():
    url = 'https://historicbet.com/cataloguer/bacbo/'
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)

    result_items = driver.find_elements(By.CSS_SELECTOR, "div.result-item")
    data = []

    for item in result_items:
        try:
            resultado = item.find_element(By.CLASS_NAME, "winner").text.strip()
            jugador = item.find_element(By.CLASS_NAME, "score").text.strip()
            hora = item.find_element(By.CLASS_NAME, "time").text.strip()
            tooltip = item.get_attribute("data-tippy-content")

            # Extraer fecha usando BeautifulSoup desde el tooltip
            soup = BeautifulSoup(tooltip, "html.parser")
            fecha_raw = soup.find("strong").text.strip()  # "6/24/2025 às 7:46:10 PM"
            fecha = fecha_raw.split(" às ")[0]

            data.append([fecha, resultado, jugador, hora])
        except Exception as e:
            print(f"Error en item: {e}")

    driver.quit()

    df = pd.DataFrame(data, columns=["Fecha", "Resultado", "Jugador", "Hora"])
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/bacbo_data.csv", index=False)
    return df
