import sys
import os
import cv2
from copy import deepcopy

sys.path.append (os.path.abspath ("../../"))
from src.communication.zmq_communicator import communicator
from src.communication.network_utils import video_reciever

class Vision_Processor:
	def __init__(self):
		self.images = {}
	
		self.settings = {}

		self.outputs = {}

		self.outputted_images = ["H_Thresh_Blur", "Src"]
	
	def process_image (self, image):
		self.images["Src"] = deepcopy (image) 

		self.images["HSV"] = cv2.cvtColor (self.images["Src"], cv2.COLOR_BGR2HSV)

		self.images["H"], self.images["S"], self.images["V"] = cv2.split (self.images["HSV"])

		ret, self.images["H_Thresh"] = cv2.threshold (self.images["H"], 100, 255, cv2.THRESH_BINARY)

		self.images["H_Thresh_Blur"] = cv2.medianBlur (self.images["H_Thresh"], 9)

		self.outputs["Circles"] = cv2.HoughCircles (self.images["H_Thresh_Blur"], cv2.cv.CV_HOUGH_GRADIENT, 2, 100) #, 200, 120)

		try:
			for i in self.outputs["Circles"][0]:
				cv2.circle (self.images["Src"], (i[0], i[1]), i[2], (0, 0, 255), thickness=2)
				print "X: {x}, Y: {y}".format (x=i[0], y=i[1])
		except:
			pass

	def show_images (self):
		if self.outputted_images:
			for key in self.outputted_images:
				try:
					cv2.imshow (key, self.images[key])
				except:
					pass
		else:
			for key in self.images.keys():
				try:
					cv2.imshow (key, self.images[key])
				except:
					pass


def main ():
	processor = Vision_Processor ()
	reciever = video_reciever ("Downward")

	#reciever.ready_up () # This is necessary since zmq will always drop the first (at least) message. This is the initial connect
	while True:
		frame = reciever.get_frame ()

		if frame is not None:
			try:
				processor.process_image (frame)
				processor.show_images ()
			except:
				pass

			key = cv2.waitKey (20)
			if key == 1048603 or key == 27:
				cv2.destroyAllWindows ()
				break

if __name__=="__main__":
	main ()
