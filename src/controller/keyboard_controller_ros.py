#!/usr/bin/env python

import rospy
import roslib

from std_msgs.msg import String
from proto2.msg import Flight_Controls

import Getch
getch = Getch._Getch ()

class keyboard_controller ():
	def __init__(self):
		self.exit = 0

		rospy.init_node ('keyboard_controller', anonymous=True)
		self.pub = rospy.Publisher ('movement/controller', Flight_Controls)

		self.printcontrols()
		while not rospy.is_shutdown() and not self.exit:
			key = getch()
			self.parsekey (key)

	def printcontrols (self):
		print "w = forward"
		print "s = backward"
		print "a = strafe left"
		print "d = strafe right"
		print "q = pivot left"
		print "e = pivot rigtht"
		print "r = ascend"
		print "f = descend"
		print "p = exit"
	def parsekey (self, key):
		# TODO: Implement ramping feature
		controls = {"Pitch":0, "Roll":0, "Yaw":0, "Z":0}
		if key.lower() == 'w':
			controls["Pitch"] = 0.5
		if key.lower() == 's':
			controls["Pitch"] = -0.5

		if key.lower() == 'a':
			controls["Roll"] = 0.5
		if key.lower() == 'd':
			controls["Roll"] = -0.5

		if key.lower() == 'q':
			controls["Yaw"] = 0.5
		if key.lower() == 'e':
			controls["Yaw"] = -0.5
	
		if key.lower() == 'r':
			controls["Z"] = 0.5
		if key.lower() == 'f':
			controls["Z"] = -0.5

		if key.lower() == 'p':
			self.exit = 1

		self.send_controls (controls)
	
	def send_controls (self, controls):
		self.pub.publish (Flight_Controls (controls["Pitch"], controls["Roll"], controls["Yaw"], controls["Z"]))
		
if __name__=="__main__":
	controller = keyboard_controller ()
