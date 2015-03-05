#!/usr/bin/python

from serial import Serial
import time
BAUDrate=115200
serialPort = Serial("/dev/ttyAMA0", BAUDrate, timeout=2)
if (serialPort.isOpen() == False):
    serialPort.open()

outStr = ''
inStr = ''

serialPort.flushInput()
serialPort.flushOutput()

#for i, a in enumerate(range(33, 126)):
#    outStr += chr(a)

#outStr = '$PMTK605*31\r\n'
#outStr = '$PMTK447*35\r\n'
#outStr = '$PMTK220,100*2F\r\n'
#outStr = '$PMTK220,200*2C\r\n'
#outStr = '$PMTK220,1000*1F\r\n'
#outStr = '$PMTK220,10000*2F\r\n'
outStr = '$PMTK314,1,1,1,1,1,5,0,0,0,0,0,0,0,0,0,0,0,0,0*2C\r\n'
#outStr = '$PMTK314,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n'
#outStr = '$PMTK251,38400*27\r\n'
#outStr = '$PMTK251,115200*1F\r\n'

serialPort.write(outStr)
time.sleep(0.1)
inStr = serialPort.read(serialPort.inWaiting())
#inStr = serialPort.readall()

print "outStr = " + outStr
print "inStr =  " + inStr

#if(inStr == outStr):
#    print "WORKED! for length of %d" % (i+1)
#else:
#    print "failed"

serialPort.close()
