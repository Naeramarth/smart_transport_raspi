import paho.mqtt.client as mqtt #import the client1
import time
import ssl

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


broker_address = "mqtt.iot-embedded.de"
port = 8883


print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_connect = on_connect
client.on_message=on_message #attach function to callback
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
client.username_pw_set("transport", "{Kaputt}")

print("connecting to broker")
client.connect(broker_address, port) #connect to broker
client.loop_start() #start the loop


print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("/trn/temp")
client.subscribe("/trn/humid")
#print("Publishing message to topic","house/bulbs/bulb1")
#client.publish("/trn/test","new success")
time.sleep(100) # wait
client.loop_stop() #stop the loop