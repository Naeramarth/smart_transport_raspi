import paho.mqtt.client as mqtt
import ssl
import time
import multiprocessing as mp
import glob
import time
import RPi.GPIO as GPIO

##############################################
#Settings
##############################################

#MQTT
broker_address = "mqtt.iot-embedded.de"
port = 8883
username = "transport"
password = "{Kaputt}"
sleep_time = 5




##############################################
#Initialize Sensors
##############################################

#Temperature
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Nach Aktivierung des Pull-UP Widerstandes wird gewartet,
# bis die Kommunikation mit dem DS18B20 Sensor aufgebaut ist
base_dir = '/sys/bus/w1/devices/'
while True:
    try:
        device_folder = glob.glob(base_dir + '28*')[0]
        break
    except IndexError:
        time.sleep(0.5)
        continue
device_file = device_folder + '/w1_slave'

# Funktion wird definiert, mit dem der aktuelle Messwert am Sensor ausgelesen werden kann
def TemperaturMessung():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Zur Initialisierung, wird der Sensor einmal "blind" ausgelesen
TemperaturMessung()

def TemperaturAuswertung():
    lines = TemperaturMessung()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = TemperaturMessung()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

#

#Publish sensor values
def publish_temp():

    temp = TemperaturAuswertung()
    client.publish("/trn/temp", temp)

def publish_humidity():


    client.publish("/trn/humid", "humid:2")

def publish_vibration():


    client.publish("/trn/vibra", "vibe:3")

def publish_preassure():


    client.publish("/trn/preassure", "preassure:4")


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
    try:

        while(True):

            output = mp.Queue()

            print("Fetching sensor data")
            processes = [mp.Process(target=publish_temp())
                         ]

            for p in processes:
                p.start()

            time.sleep(sleep_time)
    except KeyboardInterrupt
        GPIO.cleanup()