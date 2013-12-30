import zmq
import json
from time import time

class communicator ():

	"""
	zmq communicator class that takes settings from a json file
	"""

	def __init__(self, settings_file, module_name):
		# Gettings settings from settings file
		self.settings = json.load (open (settings_file, "r"))
		
		self.name = module_name
		self.port = self.settings[module_name]["Port"]
		self.log = self.settings[module_name]["Logger_File"]

		self.listeningTo = []
		if self.settings[module_name]["Listening"]:
			for module in self.settings[module_name]["Listening"]:
				self.listeningTo.append (module)

		# Setting up zmq stuff
		self.context = zmq.Context ()	
		self.Publisher = self.context.socket (zmq.PUB)
		
		self.Publisher.bind ("tcp://127.0.0.1:" + str (self.port))


	def send_message (self, msg):
		self.Publisher.send (msg)


	def get_message (self, mname=None):
		self.Subscriber = self.context.socket (zmq.SUB)
		
		for module in self.listeningTo:
			self.Subscriber.connect ("tcp://127.0.0.1:" + str (self.settings[module]["Port"]))

		if not mname:
			self.Subscriber.setsockopt (zmq.SUBSCRIBE, '')
		else:
			self.Subscriber.setsockopt (zmq.SUBSCRIBE, str (mname))

		self.msg = self.Subscriber.recv()

		return self.msg


	def get_listeningTo (self):
		return self.listeningTo


	# Needs to be modified to output as json
	def log_messages(self):
		self.log_msg = self.get_message ()
		
		with open (self.log, 'a') as self.log_file:
			self.log_file.write ("\n" + "Time: " + str (time()) + '\n' + str (self.log_msg) + "\n")
