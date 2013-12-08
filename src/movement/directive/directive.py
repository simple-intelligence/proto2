#!/usr/bin/env python

import rospy
import std_msgs.msg import String

class directive ():
	def __init__():
		# Rospy Node Info
		rospy.init_node ('movement/directive', anonymous=True)
		pub = rospy.Publisher ('movement/', Flight_Controls)
		rospy.Subscriber ('movement/controller/', Flight_Controls, callback)

	def callback(self)	
		
