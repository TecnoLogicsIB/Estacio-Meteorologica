from machine import Pin, ADC
from time import sleep, sleep_us

led = Pin(23, Pin.OUT)
sensor = ADC(Pin(34))       
sensor.atten(ADC.ATTN_11DB)     # per llegir en tot el rang de 0 a 3.3 V
sensor.width(ADC.WIDTH_12BIT)   # per ajustar la comversió AD a 12 bits (valors fins a 4095)

def recupera():
    global pols, missatge
    led.off                     
    sleep_us(280)               
    mesura = sensor.read()      
    sleep_us(40)                
    led.on                      
    sleep_us(9680)             
    tensio = mesura * (3.3 / 4095)  # V
    pols = (tensio - 0.9) / 5  # mg/m3  
    #pols = 0.170 * tensio - 0.1  # fòrmula empírica
    pols = pols * 1000         # ug/m3
    
    if (pols < 35):
        missatge = 'QUALITAT EXCEL·LENT'
    elif (pols < 75):
        missatge = 'QUALITAT BONA'
    elif (pols < 115):
        missatge = 'CONTAMINACIO LLEU'
    elif (pols < 150):
        missatge = 'CONTAMINACIO MODERADA'
    elif (pols < 250):
        missatge = 'CONTAMINACIO FORTA'
    else:
        missatge = 'CONTAMINACIO GREU'