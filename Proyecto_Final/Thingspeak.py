#!/usr/bin/python3
#BIBLIOTECAS

import RPi.GPIO as GPIO
import time, sys
import _thread
import requests
#from __future__ import print_function #Modulo para utilizar caracteristicas de python 3 en versiones inferior$import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import time,sys
from w1thermsensor import W1ThermSensor


## CONFUGURACION MQTT #----------------------------------------------------------------------------------------------------------------------------------$#  The Hostname of the ThinSpeak MQTT service
mqttHost = "mqtt.thingspeak.com"
#  Replace this with your Channel ID
channelID = "1520495"
# The Write API Key for the channel
apiKey = "87T7PC6C1FTTHAJJ"
#MQTT Connection Methods
#  Set useUnsecuredTCP to True to use the default MQTT port of 1883: This type of unsecured MQTT connection uses the least amount of system resources.
useUnsecuredTCP = False
#  Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.: Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False
#  Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.: This type of connection will use slightly more system resources, but th$#  will be secured by SSL.
useSSLWebsockets = True
##End of user configuration   ### -----------------------------------------------------------------------------------------------------------------------$

if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None
if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None
if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443

    ##Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey

#GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP) #Configurar Pin

##-----VARIABLES-GPIO-CONTROL-----##
"""
Configuracion de PIN, BOARD: https://es.pinout.xyz/
"""

##VARIABLES CONTROL-------------------------

global C        #Caudal
global count    #Flujo
global ELV
global STATE_E
global STATUS_S_IF

count = 0
C = 0
ELV = 0
STATE_E = 0
STATUS_S_IF = 0

##-----------------VARIABLES CONTROL--------------------------
#----SENSOR IF FC-50
#PIN BOARD = 15
S_IF = int(15)

#----Electrovalvula
#PIN BOARD = 13 Electrovalvula principal
A_ELV = int(13)

#----SENSOR de caudal o flujo
#PIN BOARD = 11
S_FLW = int(11)
#Funcion para calcular el flujo
def countPulse(channel):
   global count
   if start_counter == 1:
      count = count+1

#----SENSOR de Temperatura
#PIN BOARD = 13
S_TEM = W1ThermSensor() # Crear objeto para solicitar datos de temperatura al sensor

#----Electrovalvula_C	Agua caliente
PIN_Elec_V = 16

#CONFIGURACION GPIO
GPIO.setmode(GPIO.BOARD)
PINs_IN = [S_IF, S_FLW]
PINs_OUT = [A_ELV, PIN_Elec_V]

GPIO.setup(PINs_IN, GPIO.IN)
GPIO.setup(PINs_OUT, GPIO.OUT)

GPIO.add_event_detect(S_FLW, GPIO.FALLING, callback=countPulse) #Adjuntar interrupcion al pin S_FLW


#           ------      HILOS       ------
# Electrovalvula Agua Caliente
def SET_EV():
    while True:
        time.sleep(3.5)
        msg=requests.get("https://thingspeak.com/channels/1520495/field/5")
        msg=msg.json()['feeds'][-1]['field5']
        if (str(msg)=='1'):
            STATE_E = int(1)
           #print("Dentro del IF"+str(STATE_E))
        else:
            STATE_E = int(0)
        #print("hilo SET_EV, electrovalvula agua caliente"+str(msg))
        GPIO.output(PIN_Elec_V, STATE_E)

_thread.start_new_thread(SET_EV, ())

# Electrovalvula Principal
def SET_ELEC_VAL():
    while (True):
        STATUS_S_IF = GPIO.input(S_IF)
        GPIO.output(A_ELV,not(int(STATUS_S_IF)))

_thread.start_new_thread(SET_ELEC_VAL, ())  


while(True):
## ----- READ
  #Sensor de Flujo
    print("Lectura de sensores")
    #time.sleep(4)
    start_counter = 1
    time.sleep(15)
    start_counter = 0
    FLW = (count /(7.5*15))
  #Consumo
    C = round((C+(FLW)*1/60),2)
  #Temperatura
    TEMP = S_TEM.get_temperature()
    time_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
    F = open("R_Log.txt", "a")
    F.write("Consumo Total: "+str(round(C,2))+"   Litros""Flujo :" +str(round(FLW,2)) + " Litros/min"+"   Temperatura: " + str(round(TEMP,2))+"°C   " + "Activacion remota electrovalvula_C: "+ str(STATE_E) + "    Activacion local electrovalvula Principal: "+ str(STATUS_S_IF) +"  " + str(time_string) + chr(10))
    #F.write("hola"+chr(10))
    F.close()
    print("ya escribí"+chr(10))
   #Build the payload string
    #print("Inicio_Enviar_MQTT"+chr(10))
    tPayload = "field1=" + str(TEMP) + "&field2=" + str(FLW) + "&field3=" + str(C)

    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)#print("Fin_Enviar_MQTT"+chr(10))
        count=0
    except (KeyboardInterrupt):
        F.close()
        GPIO.cleanup()
        sys.exit()
        break
    except:
        print ("There was an error while publishing the data.")
        GPIO.cleanup()


