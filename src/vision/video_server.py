import sys
import os

sys.path.append (os.path.abspath ("../../"))
from src.communication.zmq_communicator import communicator
from src.communication.network_utils import video_server

def main ():
	server = video_server ("Downward")
	while True:
		server.send_frame ()

if __name__=="__main__":
	main ()
