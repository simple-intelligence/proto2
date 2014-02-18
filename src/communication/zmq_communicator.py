import sys
import os
import json
import threading
from time import time, sleep

import zmq
from debug_utils import debugging

# Finds the root of the proto2 directory
cwd = os.getcwd ().split ("/")
proto2_base_path = "/".join (cwd[0:cwd.index ("proto2") + 1])

class communicator ():
	"""
	zmq communicator class that takes settings from a json file

	Publisher has a default high-water-mark of 1000. If needed a queue system can be implemented,
	however, it is probably not necessary right now. Currently only the latest message is kept.

	Currently, if the subscriber is requesting messages faster than the publisher is publishing,
	the communicator will pass back a duplicate. This is not an issue but needs to be remembered.

	Heavily inspired by work done by Logan Evans for the Robosub of the Palouse club.
	"""

	class updater (threading.Thread):
		"""
		This is a constantly running thread that updates the currently sent msg.
		Currently it only writes to a single msg value rather than a queue but that
		can be implemented fairly easily.
		It uses a per-module update frequency to set the refresh rate
		"""
		def __init__(self, communicator, update_frequency=0.01):
			threading.Thread.__init__(self)
			self.com = communicator
			self.update_freq = update_frequency
			
		def run (self):
			while True:
				for module in self.com.get_listening_to():
					self.com.update_last_msg (module)
				sleep (self.update_freq)
	
	def __init__(self, module_name, settings_file=None):
		self.debug = debugging ()

		# Gettings settings from settings file
		if not settings_file:
			try:
				self.settings = json.load (open (proto2_base_path + "/src/communication/Communication_Settings.json", "r"))
			except:
				self.debug.print_d ("Communication_Settings.json is not in json format!")
				sys.exit ()
		else:
			try:
				self.settings = json.load (open (settings_file, "r"))
			except:
				self.debug.print_d ("Specified file [{sfile}] doesn't exist or is not in json format!".format (sfile = settings_file))
				sys.exit ()

		# Setting up publisher
		self.publisher = {}
		self.publisher["mname"] = module_name

        # TODO: Make a single context for all subscribers and one for publisher
		self.publisher["context"] = zmq.Context ()	
		self.publisher["socket"] = self.publisher["context"].socket (zmq.PUB)
		self.publisher["socket"].setsockopt (zmq.HWM, 15)
		self.publisher["socket"].bind ("tcp://" + self.settings[module_name]["IP"] + ":" + self.settings[module_name]["Port"])

		# Setting up subscribers
		self.listening_to = []
		for module in self.settings[self.publisher["mname"]]["Listening"]:
			self.listening_to.append (module)

        # TODO: Make a single context for all subscribers and one for publisher
		self.subscriber = {}
		for module in self.listening_to:
			self.subscriber[module] = {}
			self.subscriber[module]["context"] = zmq.Context ()

			self.subscriber[module]["socket"] = self.subscriber[module]["context"].socket (zmq.SUB)
			self.subscriber[module]["socket"].setsockopt (zmq.SUBSCRIBE, "")
			self.subscriber[module]["socket"].setsockopt (zmq.HWM, 15)
			self.subscriber[module]["socket"].connect ("tcp://" + self.settings[module]["IP"] + ":" + self.settings[module]["Port"])
			self.subscriber[module]["msg"] = None
				
		# Setting up refresher system
		self.refresher = self.updater (communicator=self, update_frequency=self.settings[module_name]["Update_Frequency"]) 
		self.refresher.daemon = True
		self.refresher.start()

	def get_listening_to (self):
		return self.listening_to

	def send_message (self, msg):
		msg = {"message": msg}
		msg["time"] = time ()
		msg["module"] = self.publisher["mname"]

		self.publisher["socket"].send_json (msg)

	def get_message (self, module):
		try:
			return self.subscriber[module]["msg"]
		except:
			pass	

	def update_last_msg (self, module):
		try:
			self.subscriber[module]["msg"] = self.subscriber[module]["socket"].recv_json (zmq.DONTWAIT)
		except:
			pass
