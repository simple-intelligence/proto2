import sys
import os
import threading
import json
import zmq
import cv2

from time import time, sleep
from numpy import frombuffer
from debug_utils import debugging
from zmq_communicator import communicator

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
	"""
	This will passively start getting images from the camera specified in the settings file or, if no settings file specified,
	from Video_Settings.json and send those images out using zmq. This will not run automatically when it is called.
	"""
	def __init__(self, camera, settings_file = None):
		# Gettings settings from settings file
		if not settings_file:
			# TODO: This needs fixing. Don't hardcode things like this.
			try:
				self.settings = json.load (open ("/home/dustin/programming/ros_workspace/src/proto2/src/communication/Video_Settings.json", "r"))
			except:
				self.debug.print_d ("Video_Settings.json is not in json format!")
				sys.exit ()
		else:
			try:
				self.settings = json.load (open (settings_file, "r"))
			except:
				self.debug.print_d ("Specified file [{sfile}] doesn't exist or is not in json format!".format (sfile = settings_file))
				sys.exit ()

		context = zmq.Context ()

		self.debug = debugging ()

		# Camera Settings
		self.cap = cv2.VideoCapture (self.settings[camera]["Index"])
		self.cap.set (cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.settings[camera]["Height"])
		self.cap.set (cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.settings[camera]["Width"])
		self.cap.set (cv2.cv.CV_CAP_PROP_FPS, self.settings[camera]["FPS"])
		self.cap.set (cv2.cv.CV_CAP_PROP_FOURCC, cv2.cv.CV_FOURCC (str (self.settings[camera]["Codec"][0]), str (self.settings[camera]["Codec"][1]), str (self.settings[camera]["Codec"][2]), str (self.settings[camera]["Codec"][3])))

		# ZMQ Settings	
		self.server = context.socket (zmq.PUB)
		self.server.setsockopt (zmq.HWM, self.settings[camera]["HWM"])
		self.server.bind ("tcp://" + self.settings["Server_IP"] + ":" + self.settings["Server_Port"])

		#self.confirmer = context.socket (zmq.SUB)
		#self.confirmer.setsockopt (zmq.SUBSCRIBE, "")
		#self.confirmer.connect ("tcp://" + self.settings["Reciever_IP"] + ":" + self.settings["Reciever_Port"])

		com = communicator ("Pinger_Copter")

		self.pinger = passive_pinger (communicator=com)
		self.pinger.daemon = True
		self.pinger.start ()

	def send_frame (self):
		ret, self.frame = self.cap.read ()
		if self.pinger.CONNECTED and ret:
			metadata = {}
			metadata['dtype'] = str (self.frame.dtype)
			metadata['shape'] = self.frame.shape
			try:
					self.server.send_json (metadata, flags=zmq.SNDMORE and zmq.NOBLOCK)
					self.server.send (self.frame, copy=True, track=False, flags=zmq.NOBLOCK)
			except zmq.ZMQError:
					pass

class video_reciever:
	"""
	video_reciever get images sent by the video server using settings in the file specified or in Video_Settings.json
	if no file specified
	"""
	def __init__(self, camera, settings_file = None):
		# Gettings settings from settings file
		if not settings_file:
			# TODO: This needs fixing. Don't hardcode things like this.
			try:
				self.settings = json.load (open ("/home/dustin/programming/ros_workspace/src/proto2/src/communication/Video_Settings.json", "r"))
			except:
				self.debug.print_d ("Video_settings.json is not in json format!")
				sys.exit ()
		else:
			try:
				self.settings = json.load (open (settings_file, "r"))
			except:
				self.debug.print_d ("Specified file [{sfile}] doesn't exist or is not in json format!".format (sfile = settings_file))
				sys.exit ()

		context = zmq.Context ()

		self.debug = debugging ()

		# ZMQ Settings	
		#self.confirmer = context.socket (zmq.PUB)
		#self.confirmer.bind ("tcp://" + self.settings["Reciever_IP"] + ":" + self.settings["Reciever_Port"])

		self.reciever = context.socket (zmq.SUB)
		self.reciever.setsockopt (zmq.SUBSCRIBE, "")
		self.reciever.connect ("tcp://" + self.settings["Server_IP"] + ":" + self.settings["Server_Port"])

		com = communicator ("Pinger_Base")

		self.pinger = passive_pinger (communicator=com)
		self.pinger.daemon = True
		self.pinger.start ()

		self.num_images_recieved = 0

	def get_frame (self):
		frame = None
		if self.pinger.CONNECTED:
			try:
				metadata = self.reciever.recv_json ()
				message = self.reciever.recv (copy=True, track=False)
				buf = buffer (message)		  
				frame = frombuffer (buf, dtype=metadata['dtype'])
				frame = frame.reshape (metadata['shape'])		  
				self.num_images += 1
				self.debug.print_d (num_images)
			except:
				pass
		return frame
				
