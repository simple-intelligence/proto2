import sys
import os
import threading

class passive_pinger (threading.Thread):
	def __init__(self, communicator, ping_threshold=5, ping_frequency=1):
		threading.Thread.__init__(self)

		self.com = communicator
		self.ping_frequency = ping_frequency
		self.ping_threshold = ping_threshold

		self.previous_timestamp = dict (time = 0)
		self.current_timestamp = dict (time = 9)

		self.listening_to = communicator.get_listening_to ()
		self.listening_to = self.listening_to[-1]
		print self.listening_to
		
		self.CONNECTED = False

	def run (self):
		while True:
			self.com.send_message ("")

			self.previous_timestamp = self.current_timestamp
			self.current_timestamp = self.com.get_message (self.listening_to)

			try:
				if self.current_timestamp["time"] - self.previous_timestamp["time"] < self.ping_threshold:
					self.CONNECTED = True
				else:
					self.CONNECTED = False
			except:
				self.CONNECTED = False
				pass
