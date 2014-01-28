import sys
import os
import cv2

sys.path.append (os.path.abspath ("../../"))
from src.communication.zmq_communicator import communicator
from src.communication.network_utils import video_reciever

def process_image (frame):
	
	return


def main ():
	reciever = video_reciever ("Downward")

	while True:
		frame = reciever.get_frame ()
		try:
			cv2.imshow ("frame", frame)
			process_image (frame)
		except:
			pass
		key = cv2.waitKey (20)
		if key == 1048603 or key == 27:
			cv2.destroyAllWindows ()
			break

if __name__=="__main__":
	main ()
