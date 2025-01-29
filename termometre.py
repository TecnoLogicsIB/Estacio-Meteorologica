# recuperació de dades de temperatura amb sensor DS18B20
# https://sites.google.com/xtec.cat/bellbit-g1/components/sensors-ambientals/temperatura-ds18b20 
#creat per LukasCrr i Ari

from onewire import OneWire
from ds18x20 import DS18X20 
from time import sleep
pin = Pin(19)
sensor = DS18X20(OneWire(pin))
def recupera():
    while len(sensor.scan()) == 0: 
        sleep(0.01)  
    dispositius = sensor.scan()  
    id1 = dispositius[0]
    sensor.convert_temp()
    sleep(0.75)
    global valors
    valors = round(sensor.read_temp(id1), 2)
