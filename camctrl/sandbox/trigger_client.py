"""
Title: trigger_client.py
By: ET
Description: script handles triggering camera to take a picture and updating server of new picture and when picture
             was taken.
Future Work:
-
"""

from subprocess import Popen, PIPE
import zmq

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
err_code = outpt[1]
err_code = err_code[0]
pic_loc = outpt[3].split("}")
pic_loc = pic_loc[0]

print(date)

context = zmq.Context()
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
# Send message
message_s = pic_loc + "," + date
print("Sending picture location and time-stamp: %s" % message_s)
socket.send(message_s.encode())
#  Get the reply.
message_r = socket.recv()
print("Received reply [ %s ]" % message_r)
