# recuperació de dades d'intensitat de radiació ultraviolada amb sensor GUVA-S12SD
# https://sites.google.com/xtec.cat/bellbit-g1/components/sensors-ambientals/ultraviolats-guva-s12sd
# creat per Unaiibeal i Wescraft69

from machine import Pin, ADC

sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)
sensor.width(ADC.WIDTH_10BIT)

def recupera():
    global valor,index_uv,tensio
    valor = sensor.read()
    tensio = valor * 3300/1023
    
    if (tensio < 227.0):
        index_uv = 0
    elif (tensio >= 1170.0):
        index_uv = 11
    else:
        index_uv = int((tensio-132.7)/94.3)
