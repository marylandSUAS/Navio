import time
import os

timeStart = time.time()

while True:
	if(time.time() - timeStart > 3.5):
		os.system('python trigger_v2.py')
	time.sleep(.05)
