import sys
import os
from time import sleep

sys.path.append (os.path.abspath ("../"))
from zmq_communicator import communicator


def main ():
	can = communicator ("Logger", "communication_settings.json")
	
	#logger = open (can.log, 'w')

	while True:
		for module in can.get_listening_to ():
			msg = can.get_message (module)
			print msg

		#logger.write (str (msg) + '\n')

	#logger.close ()


main ()
