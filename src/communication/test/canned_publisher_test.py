import sys
import os
from time import sleep

sys.path.append (os.path.abspath ("../"))
from zmq_communicator import communicator



def main ():
	can = communicator ("Direction", "communication_settings.json")

	print can.get_listening_to ()

	i = 0
	while True:
		msg = "Hi " + str (i)
		can.send_message (msg)
		print msg
		sleep (2)
		i += 1


main ()
