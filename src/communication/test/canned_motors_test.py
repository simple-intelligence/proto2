import sys
import os
from time import sleep

sys.path.append (os.path.abspath ("../"))
from zmq_communicator import communicator


def main ():
	can = communicator ("Motors", "communication_settings.json")

	i = 0
	while True:
		msg = can.get_message ("Direction")
		can.send_message ("Oh no we forgot the motors!!")
		print msg
		print 


main ()
