''' Visualitzador 3. Recupera les dades de Thingspeak sense pauses sleep
    Afegit: mostra de dades en pantalles LCD'''

# --- Llibreries ---
import urequests    
from time import ticks_ms, ticks_diff, sleep
from machine import Pin, I2C
import miwifi
import lcd_api      
import i2c_lcd

# --- Configuració ---
i2c1 = I2C(0, scl=Pin(22), sda=Pin(21))  
i2c2 = I2C(1, scl=Pin(18), sda=Pin(19))
lcd1 = i2c_lcd.I2cLcd(i2c1, 0x27, 2, 16)
lcd2 = i2c_lcd.I2cLcd(i2c2, 0x27, 2, 16)

# --- Variables ---
last_update = ticks_ms()
interval = 10000 

ssid = 'SSID'
psw = 'PASSWORD'
url = 'https://api.thingspeak.com/channels/1825502/feeds.json?results=1'

# --- Accions inicials ---
#lcd1.backlight_on()
#lcd2.backlight_on()
lcd1.putstr ('HOLA')
lcd2.putstr ('HOLA')

miwifi.connecta_wifi(ssid, psw)

# --- Funcions ---

def mostra():
    # mostra les dades en les LCD
    lcd1.clear()  # neteja la pantalla
    lcd2.clear()  # neteja la pantalla
    lcd1.move_to (1,0)  # posiciona el punter
    lcd1.putstr('Temp: ' + temp + ' C')
    lcd1.move_to (1,1)  # posiciona el punter
    lcd1.putstr('Llum: ' + lux + ' lx')
    lcd2.move_to (1,0)  # posiciona el punter
    lcd2.putstr('P: ' + pres + ' hPa')
    lcd2.move_to (0,1)  # posiciona el punter
    lcd2.putstr('HR: ' + hum + ' %')

def recupera():
    global temp, pres, hum, lux, uv
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
            mostra()
            last_update = ara
        except Exception as e:
            print("Error:", e)
            
