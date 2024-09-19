import requests
from bs4 import BeautifulSoup
import hashlib
import telegram
import asyncio

TELEGRAM_BOT_TOKEN = 'token'
CHAT_ID = 'chat-id'

# URL a monitorear
URL = "https://buenosaires.gob.ar/salud/plan-dengue-y-otras-enfermedades-transmitidas-por-mosquitos-aedes-aegypti/vacunacion-contra"

def get_page_hash(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    container_div = soup.find('div', class_='container')
    
    if container_div:
        page_content = container_div.get_text(strip=True)
        return hashlib.sha256(page_content.encode('utf-8')).hexdigest()
    else:
        return None

async def send_telegram_message(message):
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Error para mandar el mensaje: {e}")

async def monitor_page():
    initial_hash = get_page_hash(URL)

    while True:
        try:
            current_hash = get_page_hash(URL)

            if current_hash is None:
                await send_telegram_message("Error. No se encontró el div :(")
            elif current_hash != initial_hash:
                print("Cambios en el div perri")
                await send_telegram_message("Hubo un cambio en la página. Anda a ver!!!")
                # Update
                initial_hash = current_hash
            else:
                print("No hubo cambios u.u")
        except Exception as e:
            print(f"Hubo un error: {e}")
        
        # Espera 10 minutos
        await asyncio.sleep(600)

async def main():
    await send_telegram_message("Arrancó el bot a monitorear")
    await monitor_page()

asyncio.run(main())
