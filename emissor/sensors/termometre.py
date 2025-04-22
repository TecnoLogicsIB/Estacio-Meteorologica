# recuperació de dades de temperatura amb sensor DS18B20
# https://sites.google.com/xtec.cat/bellbit-g1/components/sensors-ambientals/temperatura-ds18b20 
#creat per LukasCrr i Ari

from onewire import OneWire
from ds18x20 import DS18X20 
from machine import Pin
from time import sleep

pin = Pin(19)
sensor = DS18X20(OneWire(pin))
valors = 0.0

while len(sensor.scan()) == 0: 
    sleep(0.01)  
dispositius = sensor.scan()
# print ('dispositius trobats:', dispositius)
id1 = dispositius[0]

def recupera():
    global id1, valors
    sensor.convert_temp()  
    sleep(0.75)
    valors = round(sensor.read_temp(id1),2)
