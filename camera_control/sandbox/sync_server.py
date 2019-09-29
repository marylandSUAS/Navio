"""
Title: sync_server.py
By: ET
Description: script handles downloading images from camera and periodically synchronizing image folder on plane with
             the ground station.

Current Work:
- Look into using pycurl
Future Work:
- Error handling when synchronization fails
"""

from subprocess import Popen, PIPE
import zmq

pic_loc_addr = "/home/pi/Pictures/"

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    while True:
        #  Wait for next request from client
        message = socket.recv()
        # print("Received picture ID and time-stamp: {}".format(message))
        #  Send reply back to client
        socket.send("Message {} received!".format(message).encode())

        # Preliminary string handling
        message = message.decode("utf-8")
        message = message.split(",")
        date = message[1]
        pic_loc = message[0]
        pic_loc = pic_loc.replace("\"","")
        pic_id = pic_loc.split("/")
        pic_id = pic_id[3]
        pic_id = pic_id.split("\"")
        pic_id = pic_id[0]

        # Download Image
        cmd = 'curl -s ' + '\"http://10.98.32.1:80' + pic_loc + '" > ' + pic_loc_addr + pic_id
        proc1 = Popen(cmd, shell=True, stdout=PIPE)
        proc1.communicate()
        proc1.wait()
        # Update Text File
        with open(pic_loc_addr + "pictures_list.txt",'a+') as list:
            list.write(pic_id + ',' + date)

        # Synchronize Filesystem with ground station (to rsync without pass, ensure ssh has ben setup on server)
        proc2 = Popen('rsync -avz -e ssh /home/pi/Pictures/ imaging@192.168.1.7:/home/imaging/imaging/Pictures',
                               shell=True, stdout=PIPE)
        stdout, stderr = proc2.communicate()
        proc2.wait()

main()