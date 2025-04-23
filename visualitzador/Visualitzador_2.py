''' Visualitzador 2. Recupera les dades de Thingspeak
    Afegit: eliminació de pauses sleep'''

# --- Llibreries ---
import urequests    
from time import ticks_ms, ticks_diff
import miwifi

# --- Configuració ---

# --- Variables ---
last_update = ticks_ms()
interval = 10000 

ssid = 'vodafoneE3D9'
psw = 'JU7AJW8YFWMWLR'
url = 'https://api.thingspeak.com/channels/1825502/feeds.json?results=1'

miwifi.connecta_wifi(ssid, psw)

# --- Funcions ---

def recupera():
    # Fer consulta a ThingSpeak
    consulta = urequests.get(url)  
    data = consulta.json()
    consulta.close()
    # recuperar les dades
    temp = data["feeds"][0]["field1"]
    pres = data["feeds"][0]["field2"]
    hum = data["feeds"][0]["field3"]
    lux = data["feeds"][0]["field4"]
    uv = data["feeds"][0]["field5"]
    # mostra per la consola
    print(temp, pres, hum, lux, uv)  

# --- Execució ---
while True:
    ara = ticks_ms()
    if ticks_diff(ara, last_update) >= interval:
        try:    
            recupera()
            last_update = ara
        except Exception as e:
            print("Error:", e)