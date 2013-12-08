#!/usr/bin/env python
import roslib
import rospy
from std_msgs.msg import String
from proto2.msg import Flight_Controls

class directive ():
	def __init__(self):
		# Rospy Node Info
		rospy.init_node ('directive', anonymous=True)
		pub = rospy.Publisher ('movement', Flight_Controls)
		rospy.Subscriber ('controller', Flight_Controls, self.callback)

	def callback(self, Controls):
		print Controls.Pitch
		print Controls.Yaw
		print Controls.Roll
		print Controls.Z


if __name__=="__main__":
	drone_control = directive ()
