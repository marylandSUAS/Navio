"""
Title: sync_v2.py
By: ET
Description: script handles downloading images from camera and updating pictures_list.txt
"""



from subprocess import Popen, PIPE
import time
import threading
import os
#import telemGrab

#telemOb = telemGrab.telemGrabOb()

#print 'continued'

pic_loc_addr = '/home/pi/Pictures/'

#grabs pics from the camera =-)
def grab_pics(line):
    #print ('GRABBER!')
    line = line.split(",")
    pic_loc = line[0]
    pic_id = pic_loc.split("/")
    pic_id = pic_id[3]
    print(pic_id)
    time_stamp = line[1]
    # data = True

    # if data:
    # Download Image
    cmd = 'curl -s ' + '\"http://10.98.32.1:80' + pic_loc + '\" > ' + pic_loc_addr + pic_id
    # print(cmd)
    proc1 = Popen(cmd, shell=True, stdout=PIPE)
    proc1.communicate()
    proc1.wait()

    # Update text file
    #print 'HERE!!'
    with open(pic_loc_addr + "pictures_list.txt", 'a+') as list:
        #print ("FALALALALA" + pic_id)
        list.write(pic_id + ',' + time_stamp + '\n')





# Clear the temp.txt file
proc1 = Popen('> ' + pic_loc_addr + 'temp.txt',shell=True, stdout=PIPE)
proc1.communicate()


pos = 0
temppos = 0

# Camera to Pi picture downloading loop
while True:
    # data = False
    # pic_loc = None
    # pic_id = None
    # time_stamp = None
    line = None
    with open(pic_loc_addr + "temp.txt", 'r+') as f:
        if temppos != pos:
            #print ('TOP O\' THE LOOP ' + str(pos))
            temppos = pos
        # Read a line
        f.seek(pos)
        line = f.readline()
        pos = f.tell()
    # String handling
    if(line != ""):
        newpid = os.fork()
        if newpid == 0:
            grab_pics(line)
            quit()
