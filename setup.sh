#Packageliste aktualisieren
echo "Packageliste wird aktualisiert..."
sudo apt-get update

#Packages upgraden
echo "Upgrade der Packages..."
sudo apt-get upgrade

#Python Pip installieren
echo "Python pip wird installiert..."
sudo apt-get install python-pip

#MQTT Paho für Python installieren
echo "MQTT Paho für Python wird installiert..."
pip install paho-mqtt

#Temperatursensor Setup
echo "Setup Temperatursensor..."
sudo sed -i '$adtoverlay=w1-gpio,gpiopin=4' /boot/config.txt
#REBOOT?

#Luftfeuchigkeit Setup
echo "Setup Luftfeuchtigkeit..."
#sudo apt-get install git --> Muss schon installiert sein
#sudo apt-get install build-essential python-dev

git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT/
sudo python setup.py install
cd ..

#Druck Setup
echo "Setup Drucksensor..."
git clone https://github.com/bastienwirtz/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP/
sudo python setup.py install
cd ..
sudo sed -i '$adtparam=i2c_arm=on' /boot/config.txt
sudo apt-get install python-smbus i2c-tools -y

#GPS Setup
echo "Setup GPS..."
sudo apt-get install gpsd gpsd-clients python-gps
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
#Initialer Start
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

#Datenbank installieren
echo "Datenbank wird installiert..."
sudo apt-get install sqlite3

#Setup Autologin


#Setup Autorun Script
sudo sed -i '$asudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock' /etc/profile
sudo sed -i '$asleep 10s' /etc/profile
sudo sed -i '$apython /smart_transport_raspi/startTransport.py' /etc/profile


#Reboot
sudo reboot




