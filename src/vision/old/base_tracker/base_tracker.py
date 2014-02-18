import sys
import os
import cv2
import numpy as np

from copy import deepcopy

sys.path.append (os.path.abspath("../../../"))
from communication.zmq_communicator import communicator

class Base_Finder:
    """
    This is all used in vision_reciever.py
    """
	def __init__(self):
		self.images = {}
	
		self.settings = {}

		self.outputs = {}

		self.outputted_images = ["Src", "Canny", "Color_Filter"]
		#self.outputted_images = None
	
		self.param1 = 200
		self.param2 = 120

	def process_image (self, image):
		self.images["Src"] = deepcopy (image) 

		self.images["Blur"] = cv2.medianBlur (self.images["Src"], 5)

		self.images["HSV"] = cv2.cvtColor (self.images["Blur"], cv2.COLOR_BGR2HSV)
		
		self.images["Color_Filter"] = cv2.inRange (self.images["HSV"], (0, 99, 99), (30, 200, 200))

		#if self.param2 == 400: self.param2 = 0
		self.images["Canny"] = cv2.Canny (self.images["Color_Filter"], 100, 200)
		#self.param2 += 1
		#print self.param2

        # Find better way. HoughCircles sucks: It is incredibly slow if many circles are found.
		self.outputs["Circles"] = cv2.HoughCircles (self.images["Color_Filter"], cv2.cv.CV_HOUGH_GRADIENT, 2, 100, param1=self.param1, param2=self.param2, minRadius=10, maxRadius=240)

		print self.outputs["Circles"]
		try:
			for i in self.outputs["Circles"][0]:
				#print i
				cv2.circle (self.images["Src"], (i[0], i[1]), i[2], (255, 0, 0), thickness=2)
				cv2.circle (self.images["Color_Filter"], (i[0], i[1]), i[2], (255, 0, 0), thickness=2)
				self.outputs["Center_Circle"] = self.outputs["Circles"][0][3].sort ()
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
	cap = cv2.VideoCapture (0)

	processor = Base_Finder ()
	while cap.isOpened():
		ret, image = cap.read ()

		processor.process_image (image)
		processor.show_images ()
		
		key = cv2.waitKey (20)
		if key == 1048603 or key == 27:
			cv2.destroyAllWindows()
			cap.release()

if __name__=="__main__":
	main ()
