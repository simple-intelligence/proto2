import sys
import Queue
import json
import threading
from time import time, sleep

import zmq
import cv2

class video_communicator:
	class network_connector (threading.Thread):
		def __init__(self, communicator, update_frequency=1):
			threading.Thread.__init__(self)
			self.com = communicator
			self.update_freq = update_frequency
	


	def __init__(self, module_name, settings_file = None, debug=False):
		# Gettings settings from settings file
		if not settings_file:
			self.settings = json.load (open ("Video_Communication_Settings.json", "r"))
		else:
			try:
				self.settings = json.load (open (settings_file, "r"))
			except:
				sys.stderr.write ("Specified file [{sfile}] doesn't exist or is not in json format!\n".format (sfile = settings_file))
				sys.exit ()

		self.CONNECTED = False

		if module_name == "Base" or module_name == "Copter":
			set_up_device (module_name)
		else:
			sys.stderr.write ("Module name must be [Base] or [Copter]") 
			sys.exit ()

		def set_up_device (self, device):
			if device == "Base":
				pinging_device = "Base"
				recieving_device = "Copter"
			else:
				pinging_device = "Copter"
				recieving_device = "Base"
				
			self.pinger["Context"] = zmq.Context ()
			self.pinger["Socket"] = self.pinger["Context"].socket (zmq.PUB)
			self.pinger["Socket"].bind ("tcp://" + self.settings[pinging_device]["IP"] + ":" + self.settings[pinging_device]["Port"])
			
			self.reciever["Context"] = zmq.Context ()
			self.reciever["Socket"] = self.reciever["Context"].socket (zmq.SUB)
			self.reciever["Socket"].setsockopt (zmq.SUBSCRIBE, "")
			self.reciever["Socket"].connect ("tcp://" + self.settings[recieving_device]["IP"] + ":" + self.settings[recieving_device]["Port"])
			
			self.current_timestamp = None

			self.connector = self.network_connector (communicator = self, self.settings ["Ping Frequency"]
			self.connector.daemon = True
			self.connector.start ()

		def send_ping (self):
			self.pinger["Socket"].send_msg (time ())
		
		def get_ping (self):
			self.current_timestamp = self.reciever["Socket"].recv (zmq.NOWAIT) 






