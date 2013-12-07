#!/usr/bin/env python

import rospy
from std_msgs.msg import String

from random import randrange, choice

def main ():
	# Just gonna publish random values now
	pub = rospy.Publisher ('move_commands', String)
	rospy.init_node ('movement')

	movement_commands = ["Yaw", "Pitch", "Roll", "Z"]

	while not rospy.is_shutdown():
		for direction in movement_commands:
			command = str (choice (movement_commands) + ": " + str ((randrange (-100, 100) / 100)))
			rospy.loginfo (command)
			pub.publish (String (command))
			rospy.sleep (1.0)

if __name__=="__main__":
	main ()
