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
		self.listening_to = self.listening_to[-1] # This only works if the pinger is only listening to a single other module (the other pinger)
		
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


class video_server:
	def __init__(self, camera, settings_file = None):,
		# Gettings settings from settings file
		if not settings_file:
			# TODO: This needs fixing. Don't hardcode things like this.
			try:
				self.settings = json.load (open ("/home/dustin/programming/ros_workspace/src/proto2/src/communication/Video_Settings.json", "r"))
			except:
				sys.stderr.write ("Communication_Settings.json is not in json format!\n")
				sys.exit ()
		else:
			try:
				self.settings = json.load (open (settings_file, "r"))
			except:
				sys.stderr.write ("Specified file [{sfile}] doesn't exist or is not in json format!\n".format (sfile = settings_file))
				sys.exit ()

		context = zmq.Context ()

		# Camera Settings
		self.cap = cv2.VideoCapture (self.settings[camera]["Index"])
		self.cap.set (cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.settings[camera]["Height"])
		self.cap.set (cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.settings[camera]["Width"])
		self.cap.set (cv2.cv.CV_CAP_PROP_FOURCC, cv2.cv.CV_FOURCC (self.settings[camera]["Codec"]))

		# ZMQ Settings	
		self.server = context.socket (zmq.PUB)
		self.server.setsockopt (zmq.HWM, self.settings[camera]["HWM"])
		self.server.bind ("tcp://" + self.settings["Server_IP"] + self.settings["Server_Port"])

		self.confirmer = context.socket (zmq.SUB)
		self.confirmer.setsockopt (zmq.SUBSCRIBE, "")
		self.confirmer.connect ("tcp://" + self.settings["Reciever_IP"] + self.settings["Reciever_Port"])

		com = communicator ("Pinger_Copter")

		pinger = passive_pinger (communicator=com)
		pinger.daemon = True
		pinger.start ()

		self.run ()

	def run (self):
		while True:
			ret, frame = self.cap.read ()
			if pinger.CONNECTED and ret:
				self.send_frame ()
			else:
				print "Not Connected!"
