import sys
import Queue
import json
import threading
from time import time, sleep

import zmq

class communicator ():
	"""
	zmq communicator class that takes settings from a json file

	Publisher has a default high-water-mark of 1000. If needed a queue system can be implemented,
	however, it is probably not necessary right now. Currently only the latest message is kept.

	Currently, if the subscriber is requesting messages faster than the publisher is publishing,
	the communicator will pass back a duplicate. This is not an issue but needs to be remembered.
	"""

	class queue_refresher (threading.Thread):
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
					self.com.update_queue (module)
				sleep (self.update_freq)
	
	def __init__(self, module_name, settings_file=None):
		# Gettings settings from settings file
		if not settings_file:
			# TODO: This needs fixing. Don't hardcode things like this.
			try:
				self.settings = json.load (open ("/home/dustin/programming/ros_workspace/src/proto2/src/communication/Communication_Settings.json", "r"))
			except:
				sys.stderr.write ("Communication_Settings.json is not in json format!\n")
				sys.exit ()
		else:
			try:
				self.settings = json.load (open (settings_file, "r"))
			except:
				sys.stderr.write ("Specified file [{sfile}] doesn't exist or is not in json format!\n".format (sfile = settings_file))
				sys.exit ()


		# Setting up publisher
		self.publisher = {}
		self.publisher["mname"] = module_name

		self.publisher["context"] = zmq.Context ()	
		self.publisher["socket"] = self.publisher["context"].socket (zmq.PUB)
		self.publisher["socket"].bind ("tcp://" + self.settings[module_name]["IP"] + ":" + self.settings[module_name]["Port"])

		# Setting up subscribers
		self.listening_to = []
		for module in self.settings[self.publisher["mname"]]["Listening"]:
			self.listening_to.append (module)

		self.subscriber = {}
		for module in self.listening_to:
			self.subscriber[module] = {}
			self.subscriber[module]["context"] = zmq.Context ()

			self.subscriber[module]["socket"] = self.subscriber[module]["context"].socket (zmq.SUB)
			self.subscriber[module]["socket"].setsockopt (zmq.SUBSCRIBE, "")
			self.subscriber[module]["socket"].connect ("tcp://" + self.settings[module]["IP"] + ":" + self.settings[module]["Port"])
			#self.subscriber[module]["queue"] = Queue.Queue () # Currently unnecessary
			self.subscriber[module]["msg"] = {}
			#self.subscriber[module]["raw_msg"] = None # Unused
				
		# Setting up refresher system
		self.refresher = self.queue_refresher (communicator=self, update_frequency=self.settings[module_name]["Update_Frequency"]) 
		self.refresher.daemon = True
		self.refresher.start()

	def get_listening_to (self):
		return self.listening_to

	def send_message (self, msg):
		if msg is not dict:
			msg = {"message": msg}
		msg["time"] = time ()
		msg["module"] = self.publisher["mname"]

		self.publisher["socket"].send_json (msg)

	def get_message (self, module):
		"""
		if not self.subscriber[module]["queue"].empty (): 
			return self.subscriber[module]["queue"].get_nowait ()
		else:
			pass
		"""
		try:
			return self.subscriber[module]["msg"]
		except:
			pass	

	def update_queue (self, module):
		"""
		try:
			self.subscriber[module]["queue"].put_nowait (self.subscriber[module]["socket"].recv_json ())
		except KeyError:
			sys.stderr.write ("[{mname}] does not subscribe to [{subscriber}]\n".format (mname = self.publisher["mname"], subscriber = module))
		"""
		try:
			self.subscriber[module]["msg"] = self.subscriber[module]["socket"].recv_json (zmq.DONTWAIT)
		except:
			pass
