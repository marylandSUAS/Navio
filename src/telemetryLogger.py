import time
import os
from pymavlink import mavutil
mav = mavutil.mavlink_connection('127.0.0.1:14550',autoreconnect=True)

os.rename('/home/pi/imaging/camera_control/Logs/telemLog_last.txt','/home/pi/imaging/camera_control/Logs/telemLog_last2.txt')
os.rename('/home/pi/imaging/camera_control/Logs/telemLog.txt','/home/pi/imaging/camera_control/Logs/telemLog_last.txt')


with open('/home/pi/imaging/camera_control/Logs/telemLog.txt','w') as locFile:
	locFile.write(str(time.time()))

while(True):
	msg = mav.recv_match(type='GLOBAL_POSITION_INT',blocking=True,timeout=5.0)
	if msg is None:
		#print 'found nothing'
		with open('/home/pi/imaging/camera_control/telemLast.txt','w') as locFile:
			locFile.write('0.0,0.0,0.0,0.0')
	else:
		telemetry = [msg.lat/(1e7),msg.lon/(1e7),msg.alt*0.00328084,msg.hdg/100.0]

		with open('/home/pi/imaging/camera_control/Logs/telemLog.txt','a+') as locFile:
			locFile.write(str(time.time()))
			locFile.write(',')
			locFile.write(str(telemetry[0]))
			locFile.write(',')
			locFile.write(str(telemetry[1]))
			locFile.write(',')
			locFile.write(str(telemetry[2]))
			locFile.write(',')
			locFile.write(str(telemetry[3]))		

		with open('/home/pi/imaging/camera_control/telemLast.txt','w') as locFile:
			locFile.write(str(telemetry[0]))
			locFile.write(',')
			locFile.write(str(telemetry[1]))
			locFile.write(',')
			locFile.write(str(telemetry[2]))
			locFile.write(',')
			locFile.write(str(telemetry[3]))
