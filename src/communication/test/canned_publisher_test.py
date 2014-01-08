import sys
import os
from time import sleep

sys.path.append (os.path.abspath ("../"))
from zmq_communicator import communicator



def main ():
	com = communicator ("Direction", settings_file="canned_communication_settings.json", debug=True)

	print com.get_listening_to ()

	i = 0
	while True:
		msg = "Hi " + str (i)
		com.send_message (msg)
		print msg
		sleep (.2)
		i += 1


main ()
