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

		self.pitch = 0
		self.roll = 0
		self.yaw = 0
		self.z = 0
		self.arm = 0

		self.control_incrementer = 0.1

		self.run ()

	def run (self):
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
		print "o = ARM"
		print "l = UNARM"
		print "p = exit"

	def parsekey (self, key):
		# TODO: Implement ramping feature
		controls = {"Pitch":0, "Roll":0, "Yaw":0, "Z":0, "Arm":0}

		controls["Pitch"] = self.pitch
		controls["Roll"] = self.roll
		controls["Yaw"] = self.yaw
		controls["Z"] = self.z
		controls["Arm"] = self.arm

		if key.lower() == 'w':
			if self.pitch < 0:
				self.pitch = 0.0
			self.pitch += self.control_incrementer

			controls["Pitch"] = self.pitch

		elif key.lower() == 's':
			if self.pitch > 0:
				self.pitch = 0.0
			self.pitch -= self.control_incrementer

			controls["Pitch"] = self.pitch

		elif key.lower() == 'a':
			if self.roll > 0:
				self.roll = 0.0
			self.roll -= self.control_incrementer

			controls["Roll"] = self.roll

		elif key.lower() == 'd':
			if self.roll < 0:
				self.roll = 0.0
			self.roll += self.control_incrementer

			controls["Roll"] = self.roll

		elif key.lower() == 'q':
			if self.yaw > 0:
				self.yaw = 0.0
			self.yaw -= self.control_incrementer

			controls["Yaw"] = self.yaw

		elif key.lower() == 'e':
			if self.yaw < 0:
				self.yaw = 0.0
			self.yaw += self.control_incrementer

			controls["Yaw"] = self.yaw
	
		elif key.lower() == 'r':
			if self.z < 0:
				self.z = 0.0
			self.z += self.control_incrementer

			controls["Z"] = self.z

		elif key.lower() == 'f':
			self.z -= self.control_incrementer
			if self.z < 0:
				self.z = 0.0

			controls["Z"] = self.z

		elif key.lower() == 'p':
			self.exit = 1
			controls = {"Pitch":0, "Roll":0, "Yaw":0, "Z":0, "Arm": 0}
			self.roll = 0
			self.pitch = 0
			self.yaw = 0
			self.z = 0
			self.arm = 0

		elif key.lower() == 'o':
			self.arm = 1

		elif key.lower() == 'l':
			self.arm = 0

		elif key.lower() == 'm':
			controls = {"Pitch":0, "Roll":0, "Yaw":0, "Z":0, "Arm": 0}
			self.roll = 0
			self.pitch = 0
			self.yaw = 0
			self.z = 0
			self.arm = 0

		else:
			controls["Pitch"] = 0
			controls["Yaw"] = 0
			controls["Roll"] = 0
			self.roll = 0
			self.pitch = 0
			self.yaw = 0

		self.sanitize_controls (controls)

	def sanitize_controls (self, controls):
		if controls["Pitch"] > 1.0:
			controls["Pitch"] = 1.0
		if controls["Pitch"] < -1.0:
			controls["Pitch"] = -1.0

		if controls["Yaw"] > 1.0:
			controls["Yaw"] = 1.0
		if controls["Yaw"] < -1.0:
			controls["Yaw"] = -1.0

		if controls["Roll"] > 1.0:
			controls["Roll"] = 1.0
		if controls["Roll"] < -1.0:
			controls["Roll"] = -1.0

		if controls["Z"] > 1.0:
			controls["Z"] = 1.0
		if controls["Z"] < -1.0:
			controls["Z"] = -1.0

		if controls["Arm"]:
			controls["Arm"] = 1 

		self.send_controls (controls)
	
	def send_controls (self, controls):
		self.com.send_message (controls)
		
if __name__=="__main__":
	controller = keyboard_controller ()
