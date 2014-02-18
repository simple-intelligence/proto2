import sys
import os
import time

sys.path.append (os.path.abspath("../../"))
from communication.zmq_communicator import communicator

class control_switcher ():
	def __init__(self):
		self.com = communicator ("Switcher")
		self.last_timestamp = 0
		self.control_msg = {"time": 0}

	def run (self):
		self.get_controls ()
		self.send_controls ()

	def get_controls (self):
        # This is where inputs are switched. Much more logic is needed here
		self.control_msg = self.com.get_message ("Controller")
		#self.control_msg = self.com.get_message ("AI")
	
	def send_controls (self):
		if self.control_msg and self.control_msg["time"] > self.last_timestamp:
			self.last_timestamp = self.control_msg["time"]
			print self.control_msg["message"]
			print 
			self.com.send_message (self.control_msg["message"])

		time.sleep (.1)

if __name__=="__main__":
	drone_control = control_switcher ()
	while True:
		drone_control.run ()
