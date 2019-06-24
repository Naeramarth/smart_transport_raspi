##############################################
#Imports
##############################################
import sensors
import GpsPoller
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


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

    try:

        #sql = 'CREATE TABLE "Values" ("Id" INTEGER NOT NULL CONSTRAINT "PK_Values" PRIMARY KEY AUTOINCREMENT "Value" REAL NOT NULL, "SensorId" INTEGER NOT NULL, "Timestamp" TEXT NOT NULL )'


        while(True):

            # Simulating Battery Life
            sensors.batteryLife = sensors.batteryLife - 0.01

            #Get Sensor Data
            temp = sensors.currTemp()
            humid = sensors.currHumid()
            preassure = sensors.currPreassure()

            #Publish MQTT
            client.publish(prefix+deviceCode+"/temp", temp)
            client.publish(prefix + deviceCode + "/humid", humid)
            client.publish(prefix + deviceCode + "/preassure", preassure)
            client.publish(prefix + deviceCode + "/battery", sensors.batteryLife)
            if GpsPoller.gpsd != None:
                latitude = GpsPoller.gpsd.fix.latitude
                longitude = GpsPoller.gpsd.fix.longitude
                client.publish(prefix + deviceCode + "/location", str(latitude)+','+str(longitude))


            #TODO: Vibration Event Data

            #TODO: Save Data to DB

            time.sleep(meassureInteval)

    except KeyboardInterrupt:
        gpsp.running = False
        gpsp.join()
        client.loop_stop()
        GPIO.cleanup()