''' Emissor 1. Recupera les dades dels sensors i envia per LoRa en format CSV
               Mostra a la consola les dades enviades '''

# import de llibreries pròpies
import barometre
import luxometre
import uv_metre
# import de llibreries de microPython
from machine import UART
from time import sleep

# --- Configuració ---
lora = UART(2, baudrate=9600, tx=17, rx=16)   # Serial UART per al mòdul LoRa

# --- Variables ---
actualitzacio = 30  # per fer proves, cada mig minut (30 s). Definitiva cada 5 minuts (300 s)

# --- Funcions ---

def recupera():  # execució de les funcions de lectura dels sensors definides en les llibreries
    barometre.recupera()
    luxometre.recupera()
    uv_metre.recupera()
    
    # definició de les variables com globals per poder utilitzar-les fora de la funció
    global temp, pres, humt, lux, uv  
    temp = barometre.temp
    #pres = round((barometre.pres / 100),2)  # per obtenir hPa amb 2 decimals
    pres = barometre.pres
    humt = barometre.humt
    lux = luxometre.lux
    uv = uv_metre.index_uv

def envia_dades():
    recupera()
    # converteix les dades a format CSV:
    dades = "{},{},{},{},{}".format(temp, pres, humt, lux, uv)
    print("Enviant:", dades)  # mostra a la consola
    lora.write(dades + "\n")  # envia amb salt de línia ("\n") per facilitar separació de missatges

# --- Execució ---
while True:
    envia_dades()
    sleep(actualitzacio)
