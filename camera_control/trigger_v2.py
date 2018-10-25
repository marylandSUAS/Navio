"""
Title: trigger_v2.py
By: ET
Description: script handles triggering camera to take a picture and updating a text file with location on camera and
             time stamp.
"""

from subprocess import Popen, PIPE

pic_loc_addr = "/home/pi/Pictures/"

# Send command to camera to take picture
addr = "http://10.98.32.1:80/ctrl/still?action=single"
proc2 = Popen(['curl',addr], stdout=PIPE, stderr=PIPE)
stdout, stderr = proc2.communicate()
outpt = stdout.decode("utf-8")

#print proc2.poll()
#print outpt
#print stderr.decode("utf-8")

# Record time
proc1 = Popen(['date'], stdout=PIPE)
stdout, stderr = proc1.communicate()
date = stdout.decode("utf-8")

# String Handling
outpt = outpt.split(":")
err_code = outpt[1]
err_code = err_code[0]
pic_loc = outpt[3].split("}")
pic_loc = pic_loc[0]
pic_loc = pic_loc.replace("\"","")

temp_txt = pic_loc + ','

#telem trigger
with open('/home/pi/camera_control/telemLast.txt','r') as locFile:
	a = locFile.readline()
temp_txt = temp_txt + a

with open(pic_loc_addr + "temp.txt", 'a+') as list:
    list.write(temp_txt)

print(temp_txt)
