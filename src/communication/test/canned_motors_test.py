import sys
import os
from time import sleep

sys.path.append (os.path.abspath ("../"))
from zmq_communicator import communicator


def main ():
	com = communicator ("Motors", settings_file="canned_communication_settings.json", debug=True)

	i = 0
	while True:
		msg = com.get_message ("Direction")
		raw_msg = com.get_message ("Direction", raw=True)
		com.send_message ("Oh no we forgot the motors!!")
		print msg
		print raw_msg
		sleep (0.5)


main ()
