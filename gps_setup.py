#!/usr/bin/python

from serial import Serial
import time
outStr = ''
inStr = ''

serialPort = Serial("/dev/ttyAMA0", 9600, timeout=2)
if (serialPort.isOpen() == False):
  serialPort.open()
serialPort.flushInput()
serialPort.flushOutput()
outStr = '$PMTK251,115200*1F\r\n'
print "outStr = " + outStr
serialPort.write(outStr)
time.sleep(0.1)
inStr = serialPort.read(serialPort.inWaiting())
print "inStr =  " + inStr
serialPort.close()


serialPort = Serial("/dev/ttyAMA0", 115200, timeout=2)
if (serialPort.isOpen() == False):
  serialPort.open()
serialPort.flushInput()
serialPort.flushOutput()
outStr = '$PMTK220,100*2F\r\n'
print "outStr = " + outStr
serialPort.write(outStr)
time.sleep(0.1)
inStr = serialPort.read(serialPort.inWaiting())
print "inStr =  " + inStr
serialPort.close()

#outStr = '$PMTK605*31\r\n'
#outStr = '$PMTK447*35\r\n'
#outStr = '$PMTK220,200*2C\r\n'
#outStr = '$PMTK220,1000*1F\r\n'
#outStr = '$PMTK220,10000*2F\r\n'
#outStr = '$PMTK314,1,1,1,1,1,5,0,0,0,0,0,0,0,0,0,0,0,0,0*2C\r\n'
#outStr = '$PMTK314,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n'
#outStr = '$PMTK251,38400*27\r\n'
