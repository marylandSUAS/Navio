
import os
import time

# move all pictures/image_locs to old folder
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
	if f.startswith('EYE')
		os.rename(f,'old/'+f)

# creates new blank image_locs
with open('/home/pi/imaging/camera_control/Pictures/image_locs.txt','w') as locFile:
	pass

# resets image logs file
with open('/home/pi/imaging/camera_control/Logs/imageLog.txt','a+') as locFile:
	pass
