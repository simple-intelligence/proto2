import sys
import os
import cv2

sys.path.append (os.path.abspath ("../../../"))
from src.communication.zmq_communicator import communicator
from src.communication.network_utils import video_reciever

def main ():
	reciever = video_reciever ("Downward")

	while True:
		frame = reciever.get_frame ()
		try:
			cv2.imshow ("frame", frame)
		except:
			pass
		cv2.waitKey (20)

if __name__=="__main__":
	main ()
