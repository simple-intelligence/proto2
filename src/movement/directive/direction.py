import sys
import os
import time

sys.path.append (os.path.abspath("../../"))
from communication.zmq_communicator import communicator

class directive ():
	def __init__(self):
		self.com = communicator ("Direction")

	def run (self):
		self.get_controls ()
		self.send_controls ()

	def get_controls (self):
		self.control_msg = self.com.get_message ("Controller")
	
	def send_controls (self):
		if self.control_msg:
			print self.control_msg["message"]
			print 
			self.com.send_message (self.control_msg["message"])
		time.sleep (1)

if __name__=="__main__":
	drone_control = directive ()
	while True:
		drone_control.run ()
