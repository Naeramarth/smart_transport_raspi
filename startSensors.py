import paho.mqtt.client as mqtt
import ssl
import multiprocessing as mp
import glob
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_BMP.BMP280 as BMP280

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

#Humidity
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11

# Hier kann der Pin deklariert werden, an dem das Sensormodul angeschlossen ist
GPIO_pin_humidity = 23

#Preassure
sensor = BMP280.BMP280()

#Vibration
GPIO_pin_vibration = 24
GPIO.setup(GPIO_pin_vibration, GPIO.IN, pull_up_down = GPIO.PUD_UP)



#Publish sensor values
def publish_temp():

    temp = TemperaturAuswertung()
    client.publish("/trn/temp", temp)

def publish_humidity():

    humidity, temp = Adafruit_DHT.read_retry(DHTSensor, GPIO_pin_humidity)
    client.publish("/trn/humid", humidity)

def publish_vibration(null):

    client.publish("/trn/vibra", "true")

def publish_preassure():

    preassure = sensor.read_pressure()
    client.publish("/trn/preassure", preassure)


#Adding for Vibration sensor
# Beim Detektieren eines Signals (fallende Signalflanke) wird die Ausgabefunktion ausgeloest
GPIO.add_event_detect(GPIO_pin_vibration, GPIO.FALLING, callback=publish_vibration, bouncetime=100)


if __name__ == '__main__':

    #Initialize MQTT Client
    client = mqtt.Client("Sensors")  # create new instance
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

#            print("Fetching sensor data")
            processes = [mp.Process(target=publish_temp()),
                         mp.Process(target=publish_humidity()),
                         mp.Process(target=publish_preassure())
                         ]

            for p in processes:
                p.start()

            time.sleep(sleep_time)
    except KeyboardInterrupt:
        GPIO.cleanup()