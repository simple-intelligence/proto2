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

		self.publisher["context"] = zmq.Context ()	
		self.publisher["socket"]= self.publisher["context"].socket (zmq.PUB)
		self.publisher["socket"].bind ("tcp://127.0.0.1:" + str (self.publisher["port"]))

		# Setting up subscribers
		self.listening_to = self.get_listening_to ()

		self.subscriber = {}
		for module in self.listening_to:
			self.subscriber[module] = {}
			self.subscriber[module]["context"] = zmq.Context ()

			self.subscriber[module]["socket"] = self.subscriber[module]["context"].socket (zmq.SUB)
			self.subscriber[module]["socket"].setsockopt (zmq.SUBSCRIBE, "")
			self.subscriber[module]["socket"].connect ("tcp://127.0.0.1:" + str (self.settings[module]["Port"]))
				

	def get_listening_to (self):
		modules = []
		if self.settings[self.publisher["mname"]]["Listening"]:
			for module in self.settings[self.publisher["mname"]]["Listening"]:
				modules.append (module)
		return modules

	def send_message (self, msg):
		if msg is not dict:
			msg = {"message": msg}
		msg ["time"] = time ()
		msg ["module"] = self.publisher["mname"]

		self.publisher["socket"].send_json (msg)

	def get_message (self, module):
		# TODO: If module is trying to get a message from a publisher that does not exist or is publishing very slowly
		# this function will wait until the message comes in. Fix this.
		try:
			return self.subscriber[module]["socket"].recv_json ()
		except KeyError:
			sys.stderr.write ("[{mname}] does not subscribe to [{subscriber}]\n".format (mname = self.publisher["mname"], subscriber = module))
			
			






