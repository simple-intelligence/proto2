import sys
import os
from time import sleep

sys.path.append (os.path.abspath ("../"))
from zmq_communicator import communicator


def main ():
	com = communicator ("Logger", settings_file="canned_communication_settings.json", debug=True)
	
	#logger = open ("proto2.log", 'w')

	while True:
		for module in com.get_listening_to ():
			msg = com.get_message (module)
			raw_msg = com.get_message (module)
			print msg
			print raw_msg
			#logger.write (str (msg) + '\n')
		sleep (1)

	#logger.close ()


main ()
