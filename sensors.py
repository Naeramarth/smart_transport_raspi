##############################################
#Imports
##############################################
import time
import RPi.GPIO as GPIO
import glob
import Adafruit_DHT
import Adafruit_BMP.BMP280 as BMP280


##############################################
#Initialize Sensors
##############################################

###### -Temperature- #########################
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

###### -Humidity- #########################

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11
# Hier kann der Pin deklariert werden, an dem das Sensormodul angeschlossen ist
GPIO_pin_humidity = 23

###### -Preassure- #########################
preassureSensor = BMP280.BMP280()

def currTemp():
    return TemperaturAuswertung()

def currHumid():
    humidity, temp = Adafruit_DHT.read_retry(DHTSensor, GPIO_pin_humidity)
    return humidity

def currPreassure():
    return preassureSensor.read_pressure()

def currLocation():
    return False