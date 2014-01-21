import sys
import os
from time import sleep

sys.path.append (os.path.abspath ("../../../"))
from communication.zmq_communicator import communicator
from communication.network_utils import passive_pinger
		
def recieve_video ():
	print "Recieving Video!"

def main ():
	com = communicator ("Pinger_Base")

	pinger = passive_pinger (communicator=com)
	pinger.daemon = True
	pinger.start ()

	while True:
		if pinger.CONNECTED:
			recieve_video ()
		else:
			print "Not Connected!"
		sleep (1)

main ()
