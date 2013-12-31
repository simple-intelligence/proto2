import sys
import os
from time import sleep

sys.path.append (os.path.abspath ("../"))
from zmq_communicator import communicator


def main ():
	com = communicator ("Logger", "canned_communication_settings.json")
	
	logger = open ("proto2.log", 'w')

	while True:
		for module in com.get_listening_to ():
			msg = com.get_message (module)
			print msg
			logger.write (str (msg) + '\n')

	logger.close ()


main ()
