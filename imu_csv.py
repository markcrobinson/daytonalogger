import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import os
import time
import math
import datetime

SETTINGS_FILE = "RTIMULib"
print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
pressure = RTIMU.RTPressure(s)

print("IMU Name: " + imu.IMUName())
print("Pressure Name: " + pressure.pressureName())

if (not imu.IMUInit()):
    print("IMU Init Failed");
    sys.exit(1)
else:
    print("IMU Init Succeeded");

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

start_time = time.time() * 1000000
print start_time
print "Time,G_X,G_Y,G_Z,R,P,Y"
while True:
  sample_time = time.time()
  if imu.IMURead():
    (x, y, z) = imu.getFusionData()
    data = imu.getIMUData()
    (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure.pressureRead()
    fusionPose = data["fusionPose"]
    #os.system('clear')

    delta = data["timestamp"] - start_time
    delta_centi = delta / 1000000.0
    print "%.2f,%.2f,%.2f,%.2f,%.1f,%.1f,%.1f" % (delta_centi,data["accel"][0],data["accel"][1],data["accel"][2],math.degrees(fusionPose[0]),math.degrees(fusionPose[1]),math.degrees(fusionPose[2]))
#    print "start_time: %i" % start_time
#    print "timestamp:  %i" % data["timestamp"]
#    print "delta:      %.2f" % delta_centi

#    print "accelValid: " + str(data["accelValid"])
#    print "accel: " + str(data["accel"])
#    print "accel x: " + str(data["accel"][0])
#    print "accel y: " + str(data["accel"][1])

#    print "compassValid: " + str(data["compassValid"])
#    print "compass: " + str(data["compass"])

#    print "fusionPoseValid: " + str(data["fusionPoseValid"])
#    print "fusionPose: " + str(data["fusionPose"])
#    print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
#    print("r: %i p: %i y: %i" % (int(math.degrees(fusionPose[0])), int(math.degrees(fusionPose[1])), int(math.degrees(fusionPose[2]))))
#    print("x: %f y: %f z: %f" % (x,y,z))

#    print "fusionQPoseValid: " + str(data["fusionQPoseValid"])
#    print "fusionQPose: " + str(data["fusionQPose"])

#    print "gyroValid: " + str(data["gyroValid"])
#    print "gyro: " + str(data["gyro"])

#    print "pressureValid: " + str(data["pressureValid"])
#    print("Pressure: %f" % (data["pressure"]))

#    print "temperatureValid: " + str(data["temperatureValid"])
#    print("Temperature: %f" % (data["temperature"]))

    #time.sleep(poll_interval*1.0/1000.0)
    time.sleep(0.02)


