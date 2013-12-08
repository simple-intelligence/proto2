#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from proto2.msg import Flight_Controls

from random import randrange, choice

def main ():
	# Just gonna publish random values now
	pub = rospy.Publisher ('movement', Flight_Controls)
	rospy.init_node ('controller')

	controls = Flight_Controls
	while not rospy.is_shutdown():
			Yaw = randrange (-100, 100) / 100.0
			Pitch = randrange (-100, 100) / 100.0
			Roll = randrange (-100, 100) / 100.0
			Z = randrange (-100, 100) / 100.0
			rospy.loginfo (Flight_Controls (Yaw, Pitch, Roll, Z))
			pub.publish (Flight_Controls (Yaw, Pitch, Roll, Z))
			rospy.sleep (1.0)

if __name__=="__main__":
	main ()
