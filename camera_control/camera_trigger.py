"""
Title: trigger_v2.py
By: ET
Description: script handles triggering camera to take a picture and updating a text file with location on camera and
             time stamp.
"""

from subprocess import Popen, PIPE
import time
import threading
import os
from sync import image_grabber

pic_loc_addr = "/home/pi/imaging/Pictures/"

image_threads = []

last_time = time.time()

while(True):

	print 'Loop finished, time taken: ',time.time()-last_time
	last_time = time.time()
	# Send command to camera to take picture
	addr = "http://10.98.32.1:80/ctrl/still?action=single"
	proc2 = Popen(['curl',addr], stdout=PIPE, stderr=PIPE)
	stdout, stderr = proc2.communicate()
	outpt = stdout.decode("utf-8")


	# String Handling
	outpt = outpt.split(":")
	err_code = outpt[1]
	err_code = err_code[0]
	pic_loc = outpt[3].split("}")
	pic_loc = pic_loc[0]
	pic_loc = pic_loc.replace("\"","")


	#telem trigger
	with open('/home/pi/imaging/camera_control/telemLast.txt','r') as locFile:
		gps_loc = locFile.readline()

	print 'image taken ',pic_loc

	image_threads.append(image_grabber(pic_loc, gps_loc,'normal'))

