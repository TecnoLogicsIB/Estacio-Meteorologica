''' Visualitzador 7. Recupera les dades de Thingspeak sense pauses sleep
    Mostra de dades en pantalles LCD
    Tira de LEDs per mostrar l'índex UV
    Mostra data i hora en OLED
    Autonomia. Sensor tàctil (TBreak) per sortir de bucle
    Afegit: mesures per reduir el consum (connexió intermitent a WiFi - lightsleep)'''

# --- Llibreries ---
import urequests    
from time import ticks_ms, ticks_diff, sleep
from machine import Pin, I2C, RTC, TouchPad, lightsleep
import miwifi
import lcd_api      
import i2c_lcd
import neopixel
import ssd1306

# --- Configuració ---
i2c1 = I2C(0, scl=Pin(22), sda=Pin(21))  
i2c2 = I2C(1, scl=Pin(18), sda=Pin(19))
lcd1 = i2c_lcd.I2cLcd(i2c1, 0x27, 2, 16)
lcd2 = i2c_lcd.I2cLcd(i2c2, 0x27, 2, 16)
leds = neopixel.NeoPixel(Pin(23), 10)  # 23: pin de connexió - 10: núm de LEDs
oled = ssd1306.SSD1306_I2C(128, 64, i2c1)  # Dimensions -en pixels- de la pantalla
Tbreak = TouchPad(Pin(15))  # sensor tàctil (connectat al pin 15)

# --- Variables ---
last_update = ticks_ms()       # per control d'actualització de l'execució
last_data_update = ticks_ms()  # pel control de l'actualització de la data/hora
interval = 10000   # funcionament definitiu: 5 minuts (300.000 ms)

ssid = 'vodafoneE3D9'
psw = 'JU7AJW8YFWMWLR'
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
oled.fill(0)             # Neteja la pantalla OLED
oled.text('HOLA', 50, 30)  # Centrat aproximadament a la part superior
oled.show()              # Mostra els canvis

for i in range(10):   # per a tots els 10 leds de la tira ...
    leds[i] = groc    # assigna un color inicial
leds.write()          # encén

#miwifi.connecta_wifi(ssid, psw)

# --- Funcions ---

def colors():
    # encen tota la tira d'un color en funció del valor recuperat de l'índex UV
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
    
def recupera_hora():
    rtc = RTC()
    return rtc.datetime()  # Retorna la data i hora en format (YYYY, MM, DD, W, HH, MM, SS, MS)

# --- Funció per mostrar data i hora en OLED
def mostra_hora():
    dt = recupera_hora()
    # Format hora i data
    hora = "{:02d}:{:02d}:{:02d}".format(dt[4], dt[5], dt[6])
    data = "{:02d}/{:02d}/{:04d}".format(dt[2], dt[1], dt[0])
    
    oled.fill(0)             # Neteja la pantalla OLED
    oled.text(hora, 30, 30)  # Centrat aproximadament a la part superior
    oled.text(data, 20, 55)  # Centrat aproximadament a la part inferior
    oled.show()              # Mostra els canvis

# --- Execució ---
while True:
    # si activem el sensor tàctil, atura l'execució del bucle:
    if Tbreak.read() < 300:  # 300: llindar entre sensor tocat / no tocat
        print("Sensor tàctil activat, aturant l'execució")
        break
    
    ara = ticks_ms()
    
    # Actualitza la data i hora cada segon
    if ticks_diff(ara, last_data_update) >= 1000:
        mostra_hora()  # Actualitza la data i hora a l'OLED
        last_data_update = ara
        
    if ticks_diff(ara, last_update) >= interval:  # interval definitiu: 5 minuts (300.000 s)
        try:
            miwifi.connecta_wifi(ssid, psw); recupera(); miwifi.desconnecta_wifi()
            mostra(); colors()
            last_update = ara
        except Exception as e:
            print("Error:", e)
    
    print ('vaig a dormir')
    lightsleep(1000)  # Dorm 100 ms abans de continuar (estalvi energètic)
    
