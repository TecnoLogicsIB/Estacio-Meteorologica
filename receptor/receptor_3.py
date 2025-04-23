''' Receptor 3. Reb dades per Lora i les mostra en la consola. Sense sleep
    Afegit: LED indicador de vida (flaix de 0.5 s) cada 5 s'''

# --- Llibreries ---
from machine import UART, Pin
from time import ticks_ms, ticks_diff

# --- Configuració ---
lora = UART(2, baudrate=9600, tx=17, rx=16)
led = Pin(23, Pin.OUT)

# --- Variables ---
temps_anterior = ticks_ms()
temps_led = ticks_ms()
interval_led = 5000       # Cada 5 segons s'encén
durada_flash = 50         # Durant 50 ms
led_actiu = False         # Estat inicial del flaix

# --- Funcions ---

def processa():
    if lora.any():  
        missatge = lora.readline()
        if missatge:
            try:
                text = missatge.decode().strip()
                print("Rebut:", text)
            except:
                print("Dades no vàlides rebudes")

# --- Execució ---
while True:
    ara = ticks_ms()
    
    # Processament LoRa:
    if ticks_diff(ara, temps_anterior) >= 100:  # actualització cada 100 ms
        processa()
        temps_anterior = ara

    # LED de vida:
    if ticks_diff(ara, temps_led) >= (durada_flash if led_actiu else interval_led):
        led.value(not led_actiu)
        led_actiu = not led_actiu
        temps_led = ara 
