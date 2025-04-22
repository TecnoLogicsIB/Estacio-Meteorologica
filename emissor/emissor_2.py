''' Emissor 2. Recupera les dades dels sensors i envia per LoRa en format CSV
               Afegit: LED indicador de dades enviades'''

# --- Llibreries ---
# llibreries pròpies
import barometre
import luxometre
import uv_metre
# llibreries de microPython
from machine import UART, Pin
from time import sleep

# --- Configuració ---
lora = UART(2, baudrate=9600, tx=17, rx=16)
led = Pin(23, Pin.OUT)

# --- Variables ---
actualitzacio = 5  # per proves: cada mig minut (30 s) - definitiu: cada 5 minuts (300 s)

# --- Funcions ---

def recupera():
    barometre.recupera()
    luxometre.recupera()
    uv_metre.recupera()
    
    global temp, pres, humt, lux, uv 
    temp = barometre.temp
    pres = barometre.pres
    humt = barometre.humt
    lux = luxometre.lux
    uv = uv_metre.index_uv
    
def envia_dades():
    recupera()
    dades = "{},{},{},{},{}".format(temp, pres, humt, lux, uv)  
    print("Enviant:", dades)
    
    # Encén el LED durant 100ms
    led.on()    # Encén el LED
    sleep(0.1)  # Manté el LED encès durant 100ms
    led.off()   # Apaga el LED
    
    lora.write(dades + "\n")  # envia amb salt de línia ("\n") per facilitar separació de missatges

# --- Execució ---
while True:
    envia_dades()
    sleep (actualitzacio)
    
