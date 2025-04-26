# importa:
import network                          # el mòdul network permet connectar en xarxa
from time import sleep                  # la classe sleep del mòdul time permet definir pauses

def connecta_wifi(ssid, psw):
    estacio = network.WLAN(network.STA_IF)  # configuració del dispositiu, que he anomenat estacio, com a estació
    estacio.active(True)                    # activa el mode estació
    estacio.connect(ssid, psw)              # connecta a la xarxa definida
    # mentre no estigui connectat ...
    while not estacio.isconnected():        # l'execució es mantindrà en aquest bucle
        print('.', end='')                    # barra de progrés (end="" fa que s'imprimeixi tot en la mateixa línia)
        sleep(0.1)                            # comprova la connexió cada 100 ms
    print('Connectat a', ssid)              # un cop connectat, mostra missatge de confirmació
    print ('la meva IP:', estacio.ifconfig()[0])
    print ('potencia senyal:', estacio.status('rssi'))
    global IP
    IP = estacio.ifconfig()[0]

def desconnecta_wifi():
    estacio = network.WLAN(network.STA_IF)  # configuració del dispositiu com a estació
    if estacio.isconnected():               # si està connectat, desconnecta
        estacio.disconnect()
        print("Desconnectat de Wi-Fi")
    estacio.active(False)
