''' Receptor 7. Reb dades per Lora i les mostra en la consola. Sense sleep
    LED indicador de vida (flaix de 0.5 s) cada 5 s
    Pujada de les dades rebudes a Thinsgpeak
    Autonomia (main.py) amb TBreak per trencar l'execució del while True
    Connexió a WiFi només quan calgui enviar dades a Thingspeak
    Afegit: Mostra dades en pantalla OLED'''

# --- Llibreries ---
from machine import UART, Pin, TouchPad, SoftI2C
from time import ticks_ms, ticks_diff
import urequests  # Llibreria per fer peticions HTTP
import miwifi     # Llibreria pròpia per connectar a la WiFi
import ssd1306    # Llibreria per treballar amb OLED

# --- Configuració ---
lora = UART(2, baudrate=9600, tx=17, rx=16)
led = Pin(23, Pin.OUT)
Tbreak = TouchPad(Pin(15))   # Definim el sensor tàctil (connectat al pin 15)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- Variables ---
temps_anterior = ticks_ms()
temps_led = ticks_ms()
interval_led = 5000       # Cada 5 segons s'encén
durada_flash = 50         # Durant 50 ms
led_actiu = False         # Estat inicial del flaix
llindar_break = 300

temp = 0
pres = 0
humt = 0
lux = 0
uv = 0

ssid = 'vodafoneE3D9'
psw = 'JU7AJW8YFWMWLR'
#ssid = 'gencat_ENS_EDU_LAB'
#psw = 'R0b0t!c@'
url = 'https://api.thingspeak.com/update?api_key=BK5LJ7G6KJN1FD3A'

IP = 'ESPERANT DADES'
dades_rebudes = 'NO'
dades_pujades = 'NO' 

# --- Funcions ---

def actualitza_oled():
    oled.fill(0)          # neteja la pantalla
    oled.text (IP, 0,10)  # mostra IP, recuperada de miwifi
    oled.text('Recepcio: ' + dades_rebudes, 0,25)
    oled.text('Pujada:   '+ dades_pujades, 0,40)
    oled.show()           # mostra el text definit

def envia_dades_thingspeak():
    global temp, pres, humt, lux, uv, IP, dades_pujades
    try:
        # associa cada variable a un cap del canal Thingspeak:
        payload = {
            'field1': temp,
            'field2': pres,
            'field3': humt,
            'field4': lux,
            'field5': uv
        }
        
        miwifi.connecta_wifi(ssid, psw)  # Connectar a Wi-Fi i enviar dades
        IP = miwifi.IP
        
        # construeix la petició:
        data = '&'.join([f"{key}={value}" for key, value in payload.items()])
        request_url = f"{url}&{data}"
        resposta = urequests.get(request_url)
        print("Resposta de ThingSpeak:", resposta.text)
        dades_pujades = resposta.text
        resposta.close()
        
        miwifi.desconnecta_wifi()  # Desconnectar Wi-Fi després de l'enviament
        
    except Exception as e:
        print("Error enviant dades a ThingSpeak:", e)
        dades_pujades = 'ERROR'

def processa():
    global temp, pres, humt, lux, uv, dades_rebudes
    if lora.any():  
        missatge = lora.readline()
        if missatge:
            try:
                text = missatge.decode().strip()
                print("Rebut:", text)
                valors = text.split(",")
                if len(valors) == 5:  # si hi ha 5 valors ...
                    temp = float(valors[0])
                    pres = float(valors[1])
                    humt = float(valors[2])
                    lux = float(valors[3])
                    uv = float(valors[4])
                    dades_rebudes = 'OK'
                    print (f"Temp: {temp} | Pressió: {pres} | Humitat: {humt} | Lux: {lux} | UV: {uv}")
                    envia_dades_thingspeak()
                else:
                    print ("Missatge incomplet o amb format incorrecte:", valors)
                    dades_rebudes = 'ERROR'
            except:
                print("Dades no vàlides rebudes")
                dades_rebudes = 'ERROR'

# --- Execució ---
while True:
    # si activem el sensor tàctil, atura l'execució del bucle:
    if Tbreak.read() < llindar_break:
        print("Sensor tàctil activat, aturant l'execució")
        break
    
    ara = ticks_ms()
    
    # Processament LoRa:
    if ticks_diff(ara, temps_anterior) >= 100:  # actualització cada 100 ms
        processa()
        actualitza_oled()
        temps_anterior = ara

    # LED de vida:
    if ticks_diff(ara, temps_led) >= (durada_flash if led_actiu else interval_led):
        led.value(not led_actiu)
        led_actiu = not led_actiu
        temps_led = ara 
