import paho.mqtt.client as mqtt
import ssl
import time
import multiprocessing as mp

#Settings
broker_address = "mqtt.iot-embedded.de"
port = 8883
username = "transport"
password = "{Kaputt}"
sleep_time = 5


#Sensor functions
def publish_temp():


    client.publish("/trn/temp", "new success")

def publish_humidity():


    client.publish("/trn/humid", "new success")

def publish_vibration():


    client.publish("/trn/vibra", "new success")

def publish_preassure():


    client.publish("/trn/preassure", "new success")


#MQTT components
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))



if __name__ == '__main__':

    #Initialize MQTT Client
    client = mqtt.Client("Sensors")  # create new instance
    client.on_connect = on_connect
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                   tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    client.username_pw_set(username, password)

    #Connect Client
    client.connect(broker_address, port)
    client.loop_start()

    #Start fetching sensor data
    while(True):

        output = mp.Queue()

        processes = [mp.Process(target=publish_temp()),
                     mp.Process(target=publish_humidity()),
                     mp.Process(target=publish_vibration()),
                     mp.Process(target=publish_preassure())
                     ]

        for p in processes:
            p.start()

        time.sleep(sleep_time)