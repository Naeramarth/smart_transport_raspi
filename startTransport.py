##############################################
#Imports
##############################################
import sensors
import GpsPoller
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import sqlite3
import datetime

##############################################
#Settings
##############################################
broker_address = "iot.eclipse.org"
port = 1883
#username = "transport"
#password = "{Kaputt}"
prefix = "/trn"
deviceCode = "/device98765"
meassureInteval = 5
securityCode = ""

##############################################
#MQTT
##############################################
def on_connect(mqttc, obj, flags, rc):
    print("Connected with RC: " + str(rc))

def on_log(mqttc, obj, level, string):
    print(string)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass

#Vibration Sensor
def publish_vibration(null):
    client.publish(prefix + deviceCode + "/vibra", True)

GPIO_pin_vibration = 24
GPIO.setup(GPIO_pin_vibration, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(GPIO_pin_vibration, GPIO.FALLING, callback=publish_vibration, bouncetime=100)



if __name__ == '__main__':

    #Connecting to MQTT Broker
    client = mqtt.Client()
    #client.on_connect = on_connect
    #client.on_publish = on_publish
    client.connect(broker_address, port, 60)
    client.loop_start()

    #GPS Poller
    gpsp = GpsPoller.GpsPoller()
    gpsp.start()


    # Database
    conn = sqlite3.connect('sensorData.db')
    conn.execute("DROP TABLE IF EXISTS 'VALUES' ")
    conn.execute("DROP TABLE IF EXISTS 'Positions' ")
    conn.execute("CREATE TABLE 'Values' ('Id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 'Sensor' CHAR(20) NOT NULL, 'Value' INTEGER, 'Timestamp' CHAR(30) NOT NULL);")
    conn.execute("CREATE TABLE 'Positions' ('Id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 'Type' CHAR(50) NOT NULL, 'Value' CHAR(50), 'Timestamp' CHAR(30) NOT NULL);")
    conn.commit()

    c = conn.cursor()

    try:

        while(True):

            # Simulating Battery Life
            sensors.batteryLife = sensors.batteryLife - 0.01

            #Get Sensor Data
            temp = sensors.currTemp()
            humid = sensors.currHumid()
            preassure = sensors.currPreassure()

            #Publish MQTT
            client.publish(securityCode + prefix + deviceCode + "/temp", temp)
            client.publish(securityCode + prefix + deviceCode + "/humid", humid)
            client.publish(securityCode + prefix + deviceCode + "/preassure", preassure)
            client.publish(securityCode + prefix + deviceCode + "/battery", sensors.batteryLife)

            # DB Insertion
            values = [("temp", temp, str(datetime.datetime.now())),
                      ("humid", humid, str(datetime.datetime.now())),
                      ("preassure", preassure, str(datetime.datetime.now())),
                      ("battery", sensors.batteryLife, str(datetime.datetime.now()))
                      ]

            c.executemany("INSERT INTO 'Values' (Sensor, Value, Timestamp) VALUES (?, ?, ?);", values)

            if GpsPoller.gpsd != None and GpsPoller.gpsd.fix.latitude != 'nan' and GpsPoller.gpsd.fix.longitude != 'nan'\
            and GpsPoller.gpsd.fix.latitude != '' and GpsPoller.gpsd.fix.longitude != '':

                latitude = GpsPoller.gpsd.fix.latitude
                longitude = GpsPoller.gpsd.fix.longitude
                client.publish(prefix + deviceCode + "/location", str(latitude)+','+str(longitude))

                positions = [   ("latitude", latitude, str(datetime.datetime.now())),
                                ("longitude", longitude, str(datetime.datetime.now()))
                             ]

                c.executemany("INSERT INTO 'Positions' (Type, Value, Timestamp) VALUES (?, ?, ?);", positions)

            conn.commit()

            #TODO: Vibration Event Data

            time.sleep(meassureInteval)

    except KeyboardInterrupt:
        conn.close()
        gpsp.running = False
        gpsp.join()
        client.loop_stop()
        GPIO.cleanup()