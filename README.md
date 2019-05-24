# smart_transport_raspi

Packages needed:

Raspi Settings to be done:
  
  For MQTT:
  
    - pip install paho-mqtt
  
  For Temperature:
  
    - Instert "dtoverlay=w1-gpio,gpiopin=4" to sudo nano /boot/config. --> reboot
    - Rpi package needed or already installed? 
    
  For Humidity:
  
    - sudo apt-get install git
    - sudo apt-get update
    - sudo apt-get install build-essential python-dev
    - git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    - cd Adafruit_Python_DHT/
    - sudo python setup.py install
    
