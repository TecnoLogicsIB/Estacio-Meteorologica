''' Receptor 2. Reb dades per Lora i les mostra en la consola
    Afegit: eliminació de pauses sleep'''

# --- Llibreries ---
from machine import UART
from time import ticks_ms, ticks_diff

# --- Configuració ---
lora = UART(2, baudrate=9600, tx=17, rx=16)

# --- Variables ---
temps_anterior = ticks_ms()

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
    if ticks_diff(ara, temps_anterior) >= 100:  # actualització cada 100 ms
        processa()
        temps_anterior = ara
