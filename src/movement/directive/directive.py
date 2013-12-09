#!/usr/bin/env python
import roslib
import rospy
from std_msgs.msg import String
from proto2.msg import Flight_Controls

class directive ():
	def __init__(self):
		# Rospy Node Info
		rospy.init_node ('directive', anonymous=True)
		pub = rospy.Publisher ('movement/directive', Flight_Controls)

		self.num_messages = 0

	def reciever (self):
		rospy.Subscriber ('movement/controller', Flight_Controls, self.callback)
		rospy.spin ()

	def callback(self, Controls):
		#print "Number of Messages: " + str (self.num_messages)
		#print "Pitch " + str (Controls.Pitch)
		#print "Yaw " + str (Controls.Yaw)
		#print "Roll " + str (Controls.Roll)
		#print "Z " + str (Controls.Z)
		#print
		self.num_messages += 1
		rospy.loginfo (Controls)


if __name__=="__main__":
	drone_control = directive ()
	while True:
		drone_control.reciever()
