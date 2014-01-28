import cv2
import numpy as np
from copy import deepcopy

class Vision_Processor ():
	def __init__(self):
		self.images = {}
	
		self.settings = {}

		self.outputted_images = None 
	
	def process_image (self, image):
		self.images["Src"] = deepcopy (image)

	def show_images (self):
		if self.outputted_images is not None:
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
	#try:
		#cap = cv2.VideoCapture (1)
	#except:
		#cap = cv2.VideoCapture (0)
	cap = cv2.VideoCapture (0)

	processor = Vision_Processor ()
	while cap.isOpened():
		ret, image = cap.read ()

		retval = processor.process_image (image)
		processor.show_images ()
		
		key = cv2.waitKey (20)
		if key == 1048603:
			cv2.destroyAllWindows()
			cap.release()

if __name__=="__main__":
	main ()
