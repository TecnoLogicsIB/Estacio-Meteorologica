''' Emissor 4. Recupera les dades dels sensors i envia per LoRa en format CSV
               LED indicador de dades enviades
               Deep Sleep entre enviaments + sensor tàctil (TBreak) per sortir de bucle
               Afegit: deepsleep cada 5 s per comprovar el sensor tàctil - recuperació i enviament de dades cada 30 s'''

# --- Llibreries ---
# import de llibreries pròpies
import barometre
import luxometre
import uv_metre
# llibreries de microPython
from machine import UART, Pin, TouchPad, deepsleep, RTC
from time import sleep

# --- Configuració ---
lora = UART(2, baudrate=9600, tx=17, rx=16)
led = Pin(23, Pin.OUT)
Tbreak = TouchPad(Pin(15))  # sensor tàctil (connectat al pin 15)
rtc = RTC()                 # RTC per guardar estat

# --- Variables ---
temps_dormir = 5000       # 5 segons = 5000 ms
interval_enviament = 6    # per fer proves, cada mig minut (30 s) == 6 fraccions de 5 s (deepsleep)
#interval_enviament = 60  # definitiu, cada 5 minuts (300 s) == 60 fraccions de 5 s (deepsleep)

# --- Funcions ---

def recupera():  # estructura recomanada, més eficient que utilitzar variables globals
    try:
        barometre.recupera()
        luxometre.recupera()
        uv_metre.recupera()
        return (
            barometre.temp,
            barometre.pres,
            barometre.humt,
            luxometre.lux,
            uv_metre.index_uv
        )
    except Exception as e:
        print("Error llegint sensors:", e)
        return None

def envia_dades():
    dades = recupera()
    
    if dades:
        missatge = "{},{},{},{},{}".format(*dades)
        print("Enviant:", missatge)
        lora.write(missatge + "\n")
    
    # Encen el LED durant 100ms
    led.on()  # Encén el LED
    sleep(0.1)  # Manté el LED encès durant 100ms
    led.off()  # Apaga el LED
    
    lora.write(dades + "\n")  # envia amb salt de línia ("\n") per facilitar separació de missatges

def obtenir_comptador():
    try:
        data = rtc.memory()
        if data:
            return int(data.decode())
    except:
        pass
    return 0

def guardar_comptador(valor):
    rtc.memory(str(valor).encode())

# --- Execució ---
while True:
    # si activem el sensor tàctil, atura l'execució del bucle:
    if Tbreak.read() < 300:  # 300: llindar entre sensor tocat / no tocat
        led.on()    # flaix llarg indicador de break
        sleep(1)
        led.off()
        sleep(0.1)  # Donar temps perquè el canvi tingui efecte abans de "morir"
        print("Sensor tàctil activat. Aturant execució.")
        break
    
    else:
        led.on()    # Encenem el LED per indicar que s'ha despertat
        sleep(0.1)
        led.off()

        # Recuperar i actualitzar comptador
        comptador = obtenir_comptador()
        comptador += 1
        print("Despertar número:", comptador)

        if comptador >= interval_enviament:  # cada tants despertars, genera i envia dades
            enviar_dades()
            comptador = 0  # Reiniciar després d'enviar

        guardar_comptador (comptador)
        print("Tornant a dormir durant 5 segons...")
        deepsleep (temps_dormir)
        
