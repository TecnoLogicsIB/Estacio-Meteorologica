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
while True:
    recupera()
    print ('temperatura =', valors, 'ºC')
    sleep (1)
