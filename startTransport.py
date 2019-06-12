##############################################
#Imports
##############################################
import sensors
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

if __name__ == '__main__':

    #Connecting to MQTT Broker
    client = mqtt.Client()
    #client.on_connect = on_connect
    #client.on_publish = on_publish
    client.connect(broker_address, port, 60)
    client.loop_start()
    try:

        while(True):

            #Get Sensor Data
            temp = sensors.currTemp()
            humid = sensors.currHumid()
            preassure = sensors.currPreassure()
            location = sensors.currLocation()

            #Publish MQTT
            client.publish(prefix+deviceCode+"/temp", temp)
            client.publish(prefix + deviceCode + "/humid", humid)
            client.publish(prefix + deviceCode + "/preassure", preassure)
            client.publish(prefix + deviceCode + "/location", location)

            #TODO: Vibration Event Data & GPS Data


            time.sleep(meassureInteval)

    except KeyboardInterrupt:
        client.loop_stop()
        GPIO.cleanup()