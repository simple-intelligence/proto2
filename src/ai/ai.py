import sys
import os
import time

sys.path.append (os.path.abspath("../"))
from communication.zmq_communicator import communicator

def main ():
	com = communicator ("AI")

	msg = {"time": 0}
	last_timestamp = 0
	control_vector = {"Yaw": 0, "Pitch": 0, "Z": 0, "Roll": 0}

	while True:
		msg = com.get_message ("Base_Finder")
		i = 0
		if msg:
			if msg["time"] > last_timestamp:
				last_timestamp = msg["time"]

				control_vector["Roll"] = 0.0
				control_vector["Yaw"] = 0.0
				control_vector["Pitch"] = 0.0
				control_vector["Z"] = 0.0

				offset = msg["message"]
				print offset
				print i
				print
				i += 1

				# TODO: Add fuzzy logic here
		
				if offset[0] == 0:
					control_vector["Roll"] = 0.0
				elif offset[0] < 0:
					control_vector["Roll"] = -0.5
				elif offset[0] > 0:
					control_vector["Roll"] = 0.5

				if offset[1] == 0:
					control_vector["Pitch"] = 0.0
				elif offset[1] < 0:
					control_vector["Pitch"] = 0.5
				elif offset[1] > 0:
					control_vector["Pitch"] = -0.5

				print control_vector
				com.send_message (control_vector)
				time.sleep (.1)

if __name__=="__main__":
	main ()
