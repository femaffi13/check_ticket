import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHAT_ID_DENISE = os.getenv("CHAT_ID_DENISE")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
service = Service(ChromeDriverManager().install()) # Configurar Selenium sin descargar el driver manualmente
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window() #Maximizar la ventana

driver.get("https://www.allaccess.com.ar/event/acdc-venta-general") 
#driver.get("https://www.allaccess.com.ar/event/airbag") 

time.sleep(5) #Esperar unos segundos para que cargue la página

def enviar_telegram(mensaje):
    token = TOKEN
    CHAT_IDS = [
        CHAT_ID,
        CHAT_ID_DENISE
    ]
    #chat_id = CHAT_ID
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    #print(url)

    # payload = {
    #     'chat_id': chat_id,
    #     'text': mensaje
    # }

    for chat_id in CHAT_IDS:
        payload = {
            'chat_id': chat_id,
            'text': mensaje
        }

        try:
            #print("📡 Enviando mensaje a Telegram...")
            response = requests.post(url, data=payload)
            #print("🔢 Código de respuesta:", response.status_code)
            #print("📦 Respuesta:", response.text)

            if response.status_code == 200:
                print("✅ Mensaje enviado correctamente.")
            else:
                print("❌ Error al enviar mensaje:", response.text)

        except Exception as e:
            print("⚠️ Excepción al enviar Telegram:", e)

try:
    soldout_div = driver.find_element(By.CLASS_NAME, "event-status.status-soldout")
    print("🎟️ El evento está agotado.")
    #enviar_telegram("Evento agotado ❌")
except NoSuchElementException:
    print("✅ El evento NO está marcado como agotado.")
    enviar_telegram("AC⚡DC 🎉 https://www.allaccess.com.ar/event/acdc-venta-general")

# Cerrar el navegador
driver.quit()