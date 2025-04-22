# recuperació de dades d'il·luminació (lux) amb sensor BH1750
# https://sites.google.com/xtec.cat/bellbit-g1/components/sensors-ambientals/llum-bh1750 
# creat per Alexjurjo i Bielesga

from machine import Pin, SoftI2C
from bh1750 import BH1750  # llibreria bh1750 desada en la carpeta lib del dispositiu

i2c = SoftI2C (scl=Pin(22), sda=Pin(21), freq=400000)
sensor = BH1750 (bus=i2c, addr=0x23)  
lux = 0.0

def recupera():
    global lux
    lux = round(sensor.luminance(BH1750.CONT_HIRES_1),2)
