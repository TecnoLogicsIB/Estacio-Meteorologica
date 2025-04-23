''' Emissor 4. Recupera les dades dels sensors i envia per LoRa en format CSV
               LED indicador de dades enviades
               Autonomia. Sensor tàctil (TBreak) per sortir de bucle
               Afegit: deepsleep entre enviaments '''

# --- Llibreries ---
# import de llibreries pròpies
import barometre
import luxometre
import uv_metre
# llibreries de microPython
from machine import UART, Pin, TouchPad, deepsleep
from time import sleep

# --- Configuració ---
lora = UART(2, baudrate=9600, tx=17, rx=16)
led = Pin(23, Pin.OUT)
Tbreak = TouchPad(Pin(15))  # sensor tàctil (connectat al pin 15)

# --- Variables ---
temps_dormir = 30000  # per fer proves, cada mig minut (30 s = 30.000 ms) - definitiu: 5 minuts (300.000 ms)

# --- Funcions ---

def recupera():  # execució de les funcions de lectura dels sensors definides en les llibreries
    barometre.recupera()
    luxometre.recupera()
    uv_metre.recupera()
    
    # definició de les variables com globals per poder utilitzar-les fora de la funció
    global temp, pres, humt, lux, uv  
    temp = barometre.temp
    pres = barometre.pres  
    humt = barometre.humt
    lux = luxometre.lux
    uv = uv_metre.index_uv

def envia_dades():
    recupera()
    # converteix les dades a format CSV:
    dades = "{},{},{},{},{}".format(temp, pres, humt, lux, uv)
    print("Enviant:", dades)  # mostra a la consola
    
    # Encen el LED durant 100ms
    led.on()  # Encén el LED
    sleep(0.1)  # Manté el LED encès durant 100ms
    led.off()  # Apaga el LED
    
    lora.write(dades + "\n")  # envia amb salt de línia ("\n") per facilitar separació de missatges

# --- Execució ---
while True:
    # si activem el sensor tàctil, atura l'execució del bucle:
    if Tbreak.read() < 300:  # 300: llindar entre sensor tocat / no tocat
        print("Sensor tàctil activat, aturant l'execució")
        break

    # si el sensor tàctil no està activat, el bucle s'executarà:
    envia_dades()
    # Activar deep sleep durant el temps definit
    print ("Entrant en Deep Sleep...")
    deepsleep (temps_dormir)  # Entrar en Deep Sleep durant el temps definit (en ms)
