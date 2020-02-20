#!/usr/bin/env python
from PIL import Image
from threading import Thread
from Queue import Queue
from time import sleep
import argparse

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Pose, PoseStamped, PointStamped, Point
from std_msgs.msg import Empty, Int32, Float32
from sensor_msgs.msg import Image as ImageR
from imaging_downlink.msg import uav_image_Msg


import os
import requests
import numpy as np
from StringIO import StringIO
import cv2
import json
from cv_bridge import CvBridge, CvBridgeError

class manager:

	def __init__(self):
		self.imQ = Queue(maxsize=1)
		self.capThread = Thread(target = self.cap_process, args = ())
		self.senderThread = Thread(target = self.ros_process, args = ())
		rospy.init_node('image_sender', anonymous=True)
		self.senderThread.start()
		self.confR = True
		rospy.Subscriber('ImageConfirm', String, self.confirmRcv)	
		self.capThread.start()


	def confirmRcv(self, thingything):
		self.confR = True
		print ("Image Received")



	def cap_process(self):
		#Capture stuff
		bridge = CvBridge()
		while (True):
			#This command captures a photo and stores the output in a
			b = os.popen("curl -s http://192.168.168.1:80/ctrl/still?action={single}")
			a = b.read()
			print (json.loads(a)["msg"])
			response = requests.get("http://192.168.168.1:80" + json.loads(a)["msg"])
			print ("ok")
			response = np.array(Image.open(StringIO(response.content)))
			print ("ok2")
			cv2.imshow(response)
			response  = bridge.cv2_to_imgmsg(response , encoding="bgr8")
			print ("ok3")
			self.imQ.put(response, True)

	def gps_process(self):
		#Capture GPS stuff
		print ("empty")

	def ros_process(self):
		#Send via ROS
		print("SenderInitialized")
		pub = rospy.Publisher('ImageSender', uav_image_Msg, queue_size=1)
		while (True):
			
			message = uav_image_Msg()
			message.image = self.imQ.get(True)
			pub.publish(message)
			self.confR = False
			while self.confR is False:
				sleep(.05)

man = manager()

