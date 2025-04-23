''' Receptor 1. Reb dades per Lora i les mostra en la consola '''

# --- Llibreries ---
from machine import UART
from time import sleep

# --- Configuració ---
lora = UART(2, baudrate=9600, tx=17, rx=16)

# --- Variables ---

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
    processa()
    sleep(0.1)
