import paho.mqtt.client as mqtt
import ssl
import multiprocessing as mp

#Settings
broker_address = "mqtt.iot-embedded.de"
port = 8883
username = "transport"
password = "{Kaputt}"


#Sensor functions
def read_temp():
    print("Temp")

def read_humidity():
    print("humidity")

def read_vibration():
    print("vibration")

def read_preassure():
    print("preassure")


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
    output = mp.Queue()

    processes = [mp.Process(target=read_temp()),
                 mp.Process(target=read_humidity()),
                 mp.Process(target=read_vibration()),
                 mp.Process(target=read_preassure())
                 ]

    for p in processes:
        p.start()