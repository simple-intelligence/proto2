import sys
import os
from time import sleep

from networker import passive_pinger
sys.path.append (os.path.abspath ("../../../"))
from communication.zmq_communicator import communicator
		
def send_video ():
	print "Sending Video!"

def main ():
	com = communicator ("Pinger_Base", debug=True)

	pinger = passive_pinger (communicator=com)
	pinger.daemon = True
	pinger.start ()

	while True:
		if pinger.CONNECTED:
			send_video ()
		else:
			print "Not Connected!"
		sleep (1)

main ()
