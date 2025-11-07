import requests
from bs4 import BeautifulSoup

def enviar_telegram(mensaje):
    token = '7785456335:AAFQCxNkifYm8teUrRgRYda8m5Mf4YV_gN0'
    chat_id = '1396394457'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': mensaje}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("📲 Mensaje enviado por Telegram.")
        else:
            print("❌ Error al enviar mensaje:", response.text)
    except Exception as e:
        print("⚠️ Excepción al enviar Telegram:", e)

# URL del evento
url = "https://www.allaccess.com.ar/event/acdc-venta-general"

# Obtener el HTML
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    print("Código de estado:", response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(response.text[:40000])  # Muestra los primeros 2000 caracteres


    # Buscar el div con clase "event-status status-soldout"
    soldout_div = soup.find("div", lambda tag: tag.get("class") and "status-soldout" in tag.get("class"))
    print(soldout_div)

    if soldout_div:
        print("🎟️ El evento está agotado.")
    else:
        print("✅ El evento NO está marcado como agotado.")
        #enviar_telegram("🎉 ¡El evento ACDC NO está agotado! Revisá AllAccess.")
except Exception as e:
    print("⚠️ Error al acceder a la página:", e)