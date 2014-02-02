import sys
import os
import cv2
from copy import deepcopy

sys.path.append (os.path.abspath ("../"))
from communication.zmq_communicator import communicator
from communication.network_utils import video_reciever

class Vision_Processor:
	def __init__(self):
		self.images = {}
	
		self.settings = {}

		self.outputs = {}

		self.outputted_images = ["H_Thresh_Blur", "Src"]
		#self.outputted_images = []
	
		self.X_Offset = 0
		self.Y_Offset = 0
		self.Radius = 0
		self.num_circles = 0

	def process_image (self, image):
		self.images["Src"] = deepcopy (image) 

		self.images["HSV"] = cv2.cvtColor (self.images["Src"], cv2.COLOR_BGR2HSV)

		self.images["H"], self.images["S"], self.images["V"] = cv2.split (self.images["HSV"])

		self.images["H_Blur"] = cv2.medianBlur (self.images["H"], 9)

		ret, self.images["H_Thresh_Blur"] = cv2.threshold (self.images["H_Blur"], 100, 255, cv2.THRESH_BINARY)

		self.outputs["Circles"] = cv2.HoughCircles (self.images["H_Thresh_Blur"], cv2.cv.CV_HOUGH_GRADIENT, 2, 5, minRadius=5, maxRadius=320)

		self.X_Offset = 0
		self.Y_Offset = 0
		self.Radius = 0
		self.num_circles = 0

		if self.outputs["Circles"] is not None:
			for i in self.outputs["Circles"][0]:
				cv2.circle (self.images["Src"], (i[0], i[1]), i[2], (0, 0, 255), thickness=2)

				self.X_Offset += i[0]
				self.Y_Offset += i[1]
				self.Radius += i[2]
				self.num_circles += 1

			if len (self.outputs["Circles"][0]) > 0 and len (self.outputs["Circles"][0]) <= 4:
				return (self.X_Offset / self.num_circles,
						self.Y_Offset / self.num_circles,
						self.Radius / self.num_circles)
			else:
				return (0, 0, 0)

		return (0, 0, 0)

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
	com = communicator ("Base_Finder")
	processor = Vision_Processor ()
	reciever = video_reciever ("Downward")

	offset = (0, 0, 0)

	#reciever.ready_up () # This is necessary since zmq will always drop the first (at least) message. This is the initial connect
	while True:
		frame = reciever.get_frame ()

		if frame is not None:
			offset = processor.process_image (frame)
			processor.show_images ()
			if offset:
				print offset

			key = cv2.waitKey (20)
			if key == 1048603 or key == 27:
				cv2.destroyAllWindows ()
				break

if __name__=="__main__":
	main ()
