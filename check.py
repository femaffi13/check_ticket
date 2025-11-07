import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.binary_location = "/usr/bin/google-chrome"

driver = webdriver.Chrome(options=chrome_options)


#driver.get("https://www.allaccess.com.ar/event/acdc-venta-general") #Abrir la página
driver.get("https://www.allaccess.com.ar/event/airbag") #Abrir la página

time.sleep(3) #Esperar unos segundos para que cargue la página

def enviar_telegram(mensaje):
    token = TOKEN
    chat_id = CHAT_ID

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': mensaje
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("📲 Mensaje enviado por Telegram.")
        else:
            print("❌ Error al enviar mensaje:", response.text)
    except Exception as e:
        print("⚠️ Excepción al enviar Telegram:", e)

try:
    soldout_div = driver.find_element(By.CLASS_NAME, "event-status.status-soldout")
    print("🎟️ El evento está agotado.")
except NoSuchElementException:
    print("✅ El evento NO está marcado como agotado.")
    enviar_telegram("🎉 ¡El evento ACDC NO está agotado! Revisá AllAccess.")

# Cerrar el navegador
driver.quit()