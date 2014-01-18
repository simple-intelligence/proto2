import sys
import os
import threading
from time import time, sleep

class passive_pinger (threading.Thread):
	def __init__(self, communicator, _ping_threshold=5, _ping_frequency=1):
		threading.Thread.__init__(self)

		self.com = communicator
		self.ping_frequency = _ping_frequency
		self.ping_threshold = _ping_threshold

		self.current_timestamp = None

		self.listening_to = communicator.get_listening_to ()
		self.listening_to = self.listening_to[-1]
		
		self.CONNECTED = False

	def run (self):
		while True:
			self.com.send_message ("")

			try:
				self.current_timestamp = self.com.get_message (self.listening_to)["time"]
			except:
				pass

			try:
				if time () - self.current_timestamp <= self.ping_threshold:
					self.CONNECTED = True
				else:
					self.CONNECTED = False
			except:
				self.CONNECTED = False
				pass

			sleep (self.ping_frequency) # IMPORTANT! time () does not like you flooding it with requests
