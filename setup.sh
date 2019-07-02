#Packageliste aktualisieren
echo "Packageliste wird aktualisiert..."
apt-get --assume-yes update

#Packages upgraden
echo "Upgrade der Packages..."
apt-get --assume-yes upgrade

#Setup Autologin
echo "Setting up Auto Login..."
systemctl set-default multi-user.target
ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service
cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf << EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $SUDO_USER --noclear %I \$TERM
EOF

#Python Pip installieren
echo "Python pip wird installiert..."
apt-get --assume-yes install python-pip

#MQTT Paho für Python installieren
echo "MQTT Paho für Python wird installiert..."
pip install paho-mqtt

#Temperatursensor Setup
echo "Setup Temperatursensor..."
sed -i '$adtoverlay=w1-gpio,gpiopin=4' /boot/config.txt
sed -i '$ai2c-dev' /etc/modules

#Luftfeuchigkeit Setup
echo "Setup Luftfeuchtigkeit..."
apt-get --assume-yes install git
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT/
python setup.py install
cd ..

#Druck Setup
echo "Setup Drucksensor..."
git clone https://github.com/bastienwirtz/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP/
python setup.py install
cd ..
sed -i '$adtparam=i2c_arm=on' /boot/config.txt
apt-get --assume-yes install python-smbus i2c-tools -y

#GPS Setup
echo "Setup GPS..."
apt-get --assume-yes install gpsd gpsd-clients python-gps
systemctl stop gpsd.socket
systemctl disable gpsd.socket
#Initialer Start
gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

#Datenbank installieren
echo "Datenbank wird installiert..."
apt-get --assume-yes install sqlite3

#Setup Autorun Script
sed -i '$asudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock' /etc/profile
sed -i '$asleep 10s' /etc/profile
sed -i '$apython smart_transport_raspi/startTransport.py &' /etc/profile

#Reboot
reboot




