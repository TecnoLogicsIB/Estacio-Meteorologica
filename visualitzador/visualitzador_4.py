''' Visualitzador 4. Recupera les dades de Thingspeak sense pauses sleep
    Mostra de dades en pantalles LCD
    Afegit: tira de LEDs per mostrar l'índex UV'''

# --- Llibreries ---
import urequests    
from time import ticks_ms, ticks_diff, sleep
from machine import Pin, I2C
import miwifi
import lcd_api      
import i2c_lcd
import neopixel

# --- Configuració ---
i2c1 = I2C(0, scl=Pin(22), sda=Pin(21))  
i2c2 = I2C(1, scl=Pin(18), sda=Pin(19))
lcd1 = i2c_lcd.I2cLcd(i2c1, 0x27, 2, 16)
lcd2 = i2c_lcd.I2cLcd(i2c2, 0x27, 2, 16)
leds = neopixel.NeoPixel(Pin(23), 10)  # 23: pin de connexió - 10: núm de LEDs

# --- Variables ---
last_update = ticks_ms()
interval = 10000 

ssid = 'SSID'
psw = 'PASSWORD'
url = 'https://api.thingspeak.com/channels/1825502/feeds.json?results=1'

# colors neopixel
lluentor = 0.1
verd = (0, int(lluentor*255), 0)
groc = (int(lluentor*255), int(lluentor*180), 0)
taronja = (int(lluentor*255), int(lluentor*100), 0)
vermell = (int(lluentor*255), 0, 0)
violeta = (int(lluentor*130), 0, int(lluentor*255))

# --- Accions inicials ---
#lcd1.backlight_on()
#lcd2.backlight_on()
lcd1.putstr ('HOLA')
lcd2.putstr ('HOLA')
for i in range(10):   # per a tots els 10 leds de la tira ...
    leds[i] = groc    # assigna un color inicial
leds.write()          # encén

miwifi.connecta_wifi(ssid, psw)

# --- Funcions ---

def colors():
    # encen tota la tira d'un color en funció del valor recuperat de l'índex UV
    # volem associar els colors al valor de uv, que s'ha recuperat en forma de text [print(type(uv))  # Veus si és str o float]
    # cal convertir-lo primer en nombre decimal (float), i després en enter (int). la conversió directa no funciona
    uv_num = float(uv)        # per comprovació: print (uv_num);print(type(uv_num))
    uv_int = int(uv_num)      # per comprovació: print(type(uv_int))
    if uv_int <= 2:
        color = verd
    elif uv_int <= 5:
        color = groc
    elif uv_int <= 7:
        color = taronja
    elif uv_int <= 10:
        color = vermell
    else:
        color = violeta
    
    for i in range(10):    # per a tots 10 leds de la tira ...
        leds[i] = color    # assigna a cada led el color corresponent
    leds.write()           # encén

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
    #uv = int(data["feeds"][0]["field5"])
    try:
        uv = int(data["feeds"][0]["field5"])
    except (ValueError, TypeError):
        uv = 0
    # mostra per la consola
    print(temp, pres, hum, lux, uv)  

# --- Execució ---
while True:
    ara = ticks_ms()
    if ticks_diff(ara, last_update) >= interval:
        try:    
            recupera()
            mostra()
            colors()
            last_update = ara
        except Exception as e:
            print("Error:", e)
            
