import zmq
import cv2
import numpy

def main ():
	context = zmq.Context (1)
	socket = context.socket (zmq.PAIR)

	socket.connect ("tcp://127.0.0.1:5001")

	metadata = {}
	while True:
		metadata = socket.recv_json ()
		message = socket.recv (copy=True, track=False)
		buf = buffer (message)	
		image = numpy.frombuffer (buf, dtype=metadata['dtype'])
		image_reshaped = image.reshape (metadata['shape'])	
		cv2.imshow ("Destination", image_reshaped)
		print type (image_reshaped)
		gray = cv2.cvtColor (image_reshaped, cv2.COLOR_BGR2GRAY)
		cv2.imshow ("Blur", gray)
		key = cv2.waitKey (10)
		if key == 1048603 or key == 27: # idk why it switches...wait...windows or linux?
			cv2.destroyAllWindows()

		
	

main ()
