''' Visualitzador 1. Recupera les dades de Thingspeak '''

# --- Llibreries ---
import urequests    # per fer peticions http
from time import sleep
import miwifi       # llibreria pròpia per connectar a WiFi

# --- Configuració ---

ssid = 'vodafoneE3D9'
psw = 'JU7AJW8YFWMWLR'
#ssid = 'gencat_ENS_EDU_LAB'
#psw = 'R0b0t!c@'
url = 'https://api.thingspeak.com/channels/1825502/feeds.json?results=1'  # adreça de recuperació de dades del canal

miwifi.connecta_wifi(ssid, psw)    # connecta a WiFi

# --- Variables ---

# --- Funcions ---

def recupera():
    #global temp, pres, hum, lux, uv  # per poder utilitzar els valors fora de la funció

    consulta = urequests.get(url)  # Fer consulta a ThingSpeak
    data = consulta.json()
    consulta.close()

    # recuperar les dades
    temp = data["feeds"][0]["field1"]
    pres = data["feeds"][0]["field2"]
    hum= data["feeds"][0]["field3"]
    lux= data["feeds"][0]["field4"]
    uv = data["feeds"][0]["field5"]
    print(temp, pres, hum, lux, uv)  # mostra per la consola

# --- Execució ---

while True:
    recupera()
    sleep (10)  # actualització cada 10 s