from machine import Pin, SoftI2C      # la classe SoftI2C permet treballar amb l'I2C 
import bme280                         # llibreria desada a la carpeta lib del dispositiu

i2c = SoftI2C (scl=Pin(22), sda=Pin(21), freq=400000)  # configuració de l'objecte i2c  
bme = bme280.BME280 (i2c=i2c)                          # configuració de l'objecte bme280
# si l'adreça del sensor no és 0x76 -> bme280: bme = bme280.BME280 (i2c=i2c, adress = adreça I2C)

def recupera():
    valors = bme.read_compensated_data()
    global temp, pres, humt
    temp = round(valors[0],2)
    pres = round((valors[1]/100),2)  # per obtenir hPa amb 2 decimals
    humt = round(valors[2],2)
