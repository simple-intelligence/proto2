import sys
import os
from time import sleep

sys.path.append (os.path.abspath ("../"))
from zmq_communicator import communicator


def main ():
	com = communicator ("Motors", "canned_communication_settings.json")

	i = 0
	while True:
		msg = com.get_message ("Direction")
		com.send_message ("Oh no we forgot the motors!!")
		print msg
		sleep (0.5)


main ()
