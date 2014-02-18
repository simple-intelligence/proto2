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

# Finds the root of the proto2 directory
cwd = os.getcwd ().split ("/")
proto2_base_path = "/".join (cwd[0:cwd.index ("proto2") + 1])

class passive_pinger (threading.Thread):
    def __init__(self, communicator, _ping_threshold=5, _ping_frequency=1):
        threading.Thread.__init__(self)

        self.com = communicator
        self.ping_frequency = _ping_frequency
        self.ping_threshold = _ping_threshold

        self.debug = debugging ()

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
                    #self.debug.print_d ("CONNECTED!")
                else:
                    self.CONNECTED = False
            except:
                self.CONNECTED = False
                #self.debug.print_d ("Not CONNECTED!")
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
            try:
                self.settings = json.load (open (proto2_base_path + "/src/communication/Video_Settings.json", "r"))
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
        #self.server.setsockopt (zmq.SNDTIMEO, 5000)
        self.server.bind ("tcp://" + self.settings["Server_IP"] + ":" + self.settings["Server_Port"])

        self.confirmer = context.socket (zmq.SUB)
        self.confirmer.setsockopt (zmq.SUBSCRIBE, "")
        #self.confirmer.setsockopt (zmq.RCVTIMEO, 5000)
        self.confirmer.connect ("tcp://" + self.settings["Reciever_IP"] + ":" + self.settings["Reciever_Port"])

        com = communicator ("Pinger_Copter")

        self.pinger = passive_pinger (communicator=com)
        self.pinger.daemon = True
        self.pinger.start ()

        self.msg = "Ready!"

    def send_frame (self):
        ret, self.frame = self.cap.read ()

        # Wait for frame Confirmation
        try:
            self.msg = self.confirmer.recv (zmq.DONTWAIT)
            #self.msg = self.confirmer.recv ()
        except:
            pass

        if self.pinger.CONNECTED and ret and self.msg == "Ready!":
            metadata = {}
            metadata['dtype'] = str (self.frame.dtype)
            metadata['shape'] = self.frame.shape
            self.debug.print_d ("Sent image!")
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
            try:
                self.settings = json.load (open (proto2_base_path + "/src/communication/Video_Settings.json", "r"))
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
        self.confirmer = context.socket (zmq.PUB)
        #self.confirmer.setsockopt (zmq.SNDTIMEO, 5000)
        self.confirmer.bind ("tcp://" + self.settings["Reciever_IP"] + ":" + self.settings["Reciever_Port"])

        self.reciever = context.socket (zmq.SUB)
        self.reciever.setsockopt (zmq.SUBSCRIBE, "")
        #self.reciever.setsockopt (zmq.RCVTIMEO, 5000)
        self.reciever.connect ("tcp://" + self.settings["Server_IP"] + ":" + self.settings["Server_Port"])

        com = communicator ("Pinger_Base")

        self.pinger = passive_pinger (communicator=com)
        self.pinger.daemon = True
        self.pinger.start ()

    def ready_up (self):
        """
        Unused
        """
        for i in range (5):
            self.confirmer.send ("Ready!")
            sleep (0.2)

    def get_frame (self):
        frame = None
        if self.pinger.CONNECTED:
            try:
                # Tell server ready to receive
                self.confirmer.send ("Ready!")

                # Recieve Image
                metadata = self.reciever.recv_json ()
                message = self.reciever.recv (copy=True, track=False)

                # Tell server to wait until buffering is finished
                self.confirmer.send ("Not ready!")

                # Buffering frame
                # This can be put into another thread to speed things up
                buf = buffer (message)
                frame = frombuffer (buf, dtype=metadata['dtype'])
                frame = frame.reshape (metadata['shape'])
                self.num_images += 1
                self.debug.print_d (num_images)

                # Ready again
                self.confirmer.send ("Ready!")

            except:
                pass
        return frame
                
