#!/bin/bash

##############################################################################
# Define variables for later
GPIO_PPS=18

##############################################################################
# Do software stuff first
apt-get update
apt-get -y install screen
if apt-get -s upgrade | grep "The following packages will be upgraded" >/dev/null; then
  apt-get -y upgrade
  apt-get -y dist-upgrade
  reboot
fi

##############################################################################
# Set up a sane environment
cat << EOF >> /etc/inputrc
# Set up pgup/pgdn
"\e[5~": history-search-backward
"\e[6~": history-search-forward
EOF
#Fix the default editor to be vim instead of nano
update-alternatives --set editor /usr/bin/vim.tiny


##############################################################################
# Disable the serial console
sed -ie "s/console=ttyAMA0,115200//" /boot/cmdline.txt
sed -ie "s/^T0/#T0/" /etc/inittab 

#Configure the PPS driver
#sed -ie "s/snd-bcm2835/pps-gpio/" /etc/modules
echo -e "\n# Enable GPIO PPS\ni$GPIO_PPS" >> /boot/config.txt

##############################################################################
# Set up i2c
apt-get -y install i2c-tools
adduser pi i2c
echo -e "\n# Enable I2C\ndtparam=i2c1=on" >> /boot/config.txt
sed -ie "/i2c-bcm2708/d" /etc/modprobe.d/raspi-blacklist.conf
sed -ie "/spi-bcm2708/d" /etc/modprobe.d/raspi-blacklist.conf

# Enable the RTC on i2c
echo -e "\n# Enable RTC overlay\dtoverlay=ds1307-rtc" >> /boot/config.txt

##############################################################################
# Install and configure GPSD
apt-get install -y gpsd gpsd-clients python-gps pps-tools

cat << EOF > /tmp/gpsd.debconf
gpsd gpsd/start_daemon boolean true
gpsd gpsd/socket string /var/run/gpsd.sock
gpsd gpsd/device string /dev/ttyAMA0
gpsd gpsd/daemon_options string "-n"
gpsd gpsd/autodetection boolean true
EOF

debconf-set-selections /tmp/gpsd.debconf
dpkg-reconfigure -f noninteractive gpsd

##############################################################################
# Rebuild NTP
sed -ie "s/^#deb-src/deb-src/" /etc/apt/sources.list
apt-get update
apt-get -y build-dep ntp
cd /tmp
apt-get -y source ntp

cd ntp*
sed -i 's/--enable-SHM/--enable-SHM --enable-ATOM/' debian/rules
sed -i "1 s/)/~pps1)/" debian/changelog 
dpkg-buildpackage -b
cd ..
dpkg -i ntp*.deb

# Configure ntp
sed -i "s/^server/#server/" /etc/ntp.conf
cat << EOF >> /etc/ntp.conf

# DS3231 RTC
server 127.127.1.0 prefer
fudge 127.127.1.0 stratum 10

# gpsd shared memory clock
server 127.127.28.0 prefer
fudge 127.127.28.0 time1 0.490 refid GPSD

# pps-gpio on /dev/pps0
server 127.127.22.0
fudge 127.127.22.0 flag3 1
EOF

#Fix the udev rule to read the time from the RTC
sed -i "s/systz/hctosys/" /lib/udev/hwclock-set

update-rc.d gpsd enable
update-rc.d fake-hwclock remove
update-rc.d hwclock.sh enable
update-rc.d ntp enable


##############################################################################
# Build RTIMULib
apt-get -y install cmake libqt4-dev python2.7-dev
cd /tmp
git clone https://github.com/richards-tech/RTIMULib
cd RTIMULib/RTIMULib/
mkdir build
cd build
cmake ..
make
make install
ldconfig
cd /tmp/RTIMULib/Linux/python/
python setup.py build
python setup.py install

##############################################################################
# Set up WiFi AP
apt-get -y install hostapd udhcpd dnsmasq

echo << EOF > /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=DaytonaLogger
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=DaytonaLogger
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

echo << EOF >> /etc/udhcp.conf
interface       wlan0
start           192.168.10.10
end             192.168.10.19
option  subnet  255.255.255.0
option  router  192.168.10.1
option  dns     192.168.10.1
option  domain  local
option  lease   86400
EOF

echo << EOF >> /etc/hosts
192.168.10.1	daytonalogger.local daytonalogger
192.168.10.10	client10.local client10
192.168.10.11	client11.local client11
192.168.10.12	client12.local client12
192.168.10.13	client13.local client13
192.168.10.14	client14.local client14
192.168.10.15	client15.local client15
192.168.10.16	client16.local client16
192.168.10.17	client17.local client17
192.168.10.18	client18.local client18
192.168.10.19	client19.local client19
EOF


