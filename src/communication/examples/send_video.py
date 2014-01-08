import sys
import zmq
import cv2
import numpy as np

def send_image (image, socket):
	metadata = {}
	metadata['dtype'] = str (image.dtype)
	metadata['shape'] = image.shape
	try:
		socket.send_json (metadata, flags=zmq.SNDMORE and zmq.NOBLOCK)
		socket.send (image, copy=True, track=False, flags=zmq.NOBLOCK)
	except zmq.ZMQError:
		sys.stderr.write ("Image not sent!\n")
		pass

if __name__=="__main__":
	cap = cv2.VideoCapture (0)
	context = zmq.Context (1)
	socket = context.socket (zmq.PAIR)
	socket.bind ("tcp://127.0.0.1:5001")
	while True:
		ret, image = cap.read ()
		#cv2.imshow ("Source", image)

		if ret:
			send_image (image, socket)
		
		key = cv2.waitKey (20)
		if key == 1048603 or key == 27: # idk why it switches...wait...windows or linux?
			cv2.destroyAllWindows()
			cap.release()

