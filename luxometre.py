# creat per Alexjurjo i Bielesga

from machine import Pin, SoftI2C
from bh1750 import BH1750

i2c = SoftI2C (scl=Pin(22), sda=Pin(21), freq=400000)
sensor = BH1750 (bus=i2c, addr=0x23)    
