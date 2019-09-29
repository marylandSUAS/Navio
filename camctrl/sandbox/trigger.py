"""
By: ET
Description: script handles triggering camera to take a picture and recording when picture was taken

Future Work:
- error handling when command to take picture fails
"""

from subprocess import Popen, PIPE
import string

# Record time
proc1 = Popen(['date'], stdout=PIPE)
stdout, stderr = proc1.communicate()
date = stdout.decode("utf-8")

# Send command to camera to take picture
addr = "http://10.98.32.1:80/ctrl/still?action=single"
proc2 = Popen(['curl',addr], stdout=PIPE, stderr=PIPE)
stdout, stderr = proc2.communicate()
outpt = stdout.decode("utf-8")

# String Handling
outpt = outpt.split(":")
"""
'code' indicates whether or not the command was successfully sent
"""
err_code = outpt[1]
err_code = err_code[0]
"""
'pic_id' holds string of picture just taken
"""
pic_loc = outpt[3].split("}")
pic_loc = pic_loc[0]


print(date)
print(err_code)
print(pic_loc)