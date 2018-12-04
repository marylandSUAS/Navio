#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Pose, PoseStamped, PointStamped, Point
from std_msgs.msg import Empty, Int32, Float32
from sensor_msgs.msg import Image
from imaging_downlink.msg import uav_image_Msg

import cv2
import numpy as np
import time
import os
import sys
import signal
from cv_bridge import CvBridge, CvBridgeError


def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    print('booyah! bye bye')
    sys.exit(1)


signal.signal(signal.SIGINT, sigterm_handler)




class image_sender:

	#self always goes first
	def confirm(self, Empty):
		print('confirmed')
		self.booley = True




	

	def image_sender_method(self):
		while True:
			time.sleep(.05)	
			file_list = os.listdir("/home/imaging/PlanePics")		
			for filey in file_list:
				if filey not in self.sentfiles:
					print filey
					self.bridge = CvBridge()
					self.img = cv2.imread('/home/imaging/PlanePics/'+filey, 1)
					output_im = self.bridge.cv2_to_imgmsg(self.img, encoding="bgr8")
					self.sentfiles.append(filey)	

					pois = Point(1,2,3)

					message = uav_image_Msg()
					message.image = output_im
					message.pos = pois

					rospy.loginfo(message)
					self.booley = False	
					self.pub.publish(message) 
					while self.booley == False:
						time.sleep(.05)
			
	
				
		
	


	def __init__(self):
		
		rospy.init_node('image_sender_thing', anonymous=True)
		rospy.Subscriber('ImageConfirm', Empty, self.confirm)	
		self.pub = rospy.Publisher('ImageSender', uav_image_Msg, queue_size=1)
		self.booley = True
		self.sentfiles = []
		self.image_sender_method()
	

image_sender()

