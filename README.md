# Estacio-Meteorològica
<p>ESP32 amb microPython. 1r Batxillerat Tecnològic Institut Bellvitge.<br>
<a href="https://sites.google.com/xtec.cat/bellbit-g1/seqüència-daprenentatge/mesurem-lambient" target="_blank">e-spai d'aprenentatge</a> - <a href="https://thingspeak.mathworks.com/channels/1825502" target="_blank">canal de Thingspeak</a></p> 

<p><b>Seqüència de treball:</b><br>
Mesurem l'ambient (recuperem dades dels sensors)<br>
Connectem-lo com a estació a una xarxa WiFi<br>
Fem-lo treballar com a client HTTP<br>
Pugem dades al núvol (Thingspeak)<br>
Solucionem problemes de connectivitat WiFi:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Emissor LoRa (sense connectivitat WiFi) -> llegeix els sensors i envia les dades via LoRa<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Receptor LoRa (amb connectivitat WiFi) -> reb les dades i les envia a un canal de Thingspeak</p>
