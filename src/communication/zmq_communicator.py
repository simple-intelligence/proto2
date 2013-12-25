import sys
import json
from time import time

import zmq

class communicator ():
	"""
	zmq communicator class that takes settings from a json file
	"""
	def __init__(self, module_name, settings_file=None):
		# Gettings settings from settings file
		if not settings_file:
			self.settings = json.load (open ("Communication_Settings.json", "r"))
		else:
			try:
				self.settings = json.load (open (settings_file, "r"))
			except:
				sys.stderr.write ("Specified file [{sfile}] doesn't exist or is not in json format!\n".format (sfile = settings_file))
				sys.exit ()
		
		# Setting up publisher
		self.publisher = {}
		self.publisher["mname"] = module_name
		self.publisher["port"] = self.settings[module_name]["Port"]

		self.context = zmq.Context ()	
		self.Publisher = self.context.socket (zmq.PUB)
		self.Publisher.bind ("tcp://127.0.0.1:" + str (self.port))

		# Setting up subscribers
		self.listening_to = get_listening_to ()

		self.subscriber = {}
		for module in self.listening_to:
			self.subscriber[module]["context"] = zmq.Context ()

			self.subscriber[module]["socket"] = self.subscriber[module]["context"].socket (zmq.SUB)
			self.subscriber[module]["socket"].setsockopt (zmq.SUBSCRIBE)
			self.subscriber[module]["socket"].connect ("tcp://127.0.0.1:" + self.settings[module]["port"])
				

	def get_listening_to (self):
		modules = []
		if self.settings[module_name]["Listening"]:
			for module in self.settings[module_name]["Listening"]:
				modules.append (module)
		return modules

		

		
		



i = communicator ("test", "test1")
