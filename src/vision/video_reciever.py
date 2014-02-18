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
	
		self.X_pos = 0
		self.Y_pos = 0
		self.Radius = 0
		self.num_circles = 0

	def process_image (self, image):
		self.images["Src"] = deepcopy (image) 

		self.images["HSV"] = cv2.cvtColor (self.images["Src"], cv2.COLOR_BGR2HSV)

		self.images["H"], self.images["S"], self.images["V"] = cv2.split (self.images["HSV"])

		self.images["H_Blur"] = cv2.medianBlur (self.images["H"], 9)

		ret, self.images["H_Thresh_Blur"] = cv2.threshold (self.images["H_Blur"], 100, 255, cv2.THRESH_BINARY)

		self.outputs["Circles"] = cv2.HoughCircles (self.images["H_Thresh_Blur"], cv2.cv.CV_HOUGH_GRADIENT, 2, 5, minRadius=5, maxRadius=320)

		self.X_pos = 0
		self.Y_pos = 0
		self.Radius = 0
		self.num_circles = 0

		if self.outputs["Circles"] is not None:
			for i in self.outputs["Circles"][0]:
				cv2.circle (self.images["Src"], (i[0], i[1]), i[2], (0, 0, 255), thickness=2)
				#print "{a}, {b}".format (a=i[0] - 320, b=i[1] - 240)

				if self.num_circles < 4:
					self.X_pos += i[0]
					self.Y_pos += i[1]
					self.Radius += i[2]
					self.num_circles += 1
				else:
					pass

			#print "avg: {a}, {b}".format (a=(self.X_pos / self.num_circles) - 320, b=(self.Y_pos / self.num_circles) - 240)
			#print self.num_circles
			#print

			return (int (self.X_pos / self.num_circles) - 320,
					int (self.Y_pos / self.num_circles) - 240,
					int (self.Radius / self.num_circles))

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

	pos = (0, 0, 0)

	while True:
		frame = reciever.get_frame ()

		if frame is not None:
			pos = processor.process_image (frame)
			processor.show_images ()
			if pos:
				#print pos
				com.send_message (pos)

			key = cv2.waitKey (20)
			if key == 1048603 or key == 27:
				cv2.destroyAllWindows ()
				break

if __name__=="__main__":
	main ()
