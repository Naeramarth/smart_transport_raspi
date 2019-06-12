# smart_transport_raspi

To Be Done:
  
  For MQTT:
  
    - pip install paho-mqtt
  
  For Temperature:
  
    - Instert "dtoverlay=w1-gpio,gpiopin=4" to sudo nano /boot/config.txt --> reboot
    - Rpi package needed or already installed? 
    
  For Humidity:
  
    - sudo apt-get install git
    - sudo apt-get update
    - sudo apt-get install build-essential python-dev
    - git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    - cd Adafruit_Python_DHT/
    - sudo python setup.py install
    
  For Preassure:
  
    - git clone https://github.com/bastienwirtz/Adafruit_Python_BMP.git
    - cd Adafruit_Python_BMP/
    - sudo python setup.py install
    - Instert "dtparam=i2c_arm=on" to sudo nano /boot/config.txt --> reboot
    - sudo apt-get install python-smbus i2c-tools -y
    
  For GPS:
  
    - sudo apt-get install gpsd gpsd-clients python-gps
    - sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
    - Help: http://wiki.dragino.com/index.php?title=Getting_GPS_to_work_on_Raspberry_Pi_3_Model_B
