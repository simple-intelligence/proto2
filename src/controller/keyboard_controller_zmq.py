import sys
import os

import Getch
getch = Getch._Getch ()

sys.path.append (os.path.abspath("../"))
from communication.zmq_communicator import communicator

class keyboard_controller ():
	def __init__(self):
		self.exit = 0

		self.com = communicator ("Controller")

		self.printcontrols()
		while not self.exit:
			key = getch()
			print key
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
		elif key.lower() == 's':
			controls["Pitch"] = -0.5

		elif key.lower() == 'a':
			controls["Roll"] = 0.5
		elif key.lower() == 'd':
			controls["Roll"] = -0.5

		elif key.lower() == 'q':
			controls["Yaw"] = 0.5
		elif key.lower() == 'e':
			controls["Yaw"] = -0.5
	
		elif key.lower() == 'r':
			controls["Z"] = 0.5
		elif key.lower() == 'f':
			controls["Z"] = -0.5

		elif key.lower() == 'p':
			self.exit = 1
		else:
			controls = {"Pitch":0, "Roll":0, "Yaw":0, "Z":0}

		self.send_controls (controls)
	
	def send_controls (self, controls):
		self.com.send_message (controls)
		
if __name__=="__main__":
	controller = keyboard_controller ()
