#!/usr/bin/env python

import math
from copy import deepcopy

import cv2
import numpy as np

from simple_geometry import pt, line, tri, directions
import profile

class Base_Tracker ():
	def __init__(self, cap, debug=0):
		self.LEDS_FOUND = 0

		# Image
		self.images = {}

		# Resolution of image
		self.COLS = cap.get (3)
		self.ROWS = cap.get (4)

		# Sending to movement module	
		self.Instructions = directions ()

		# Geometry
		self.led_pos = [] # array of tuples
		self.led_pts = [] # array of pts

		self.midpoint = None # pt
		self.opposite_pt = None # pt
		self.hypotenuse = None # line
		self.base_tri = None # tri

		self.offset_from_base = 0
		self.twist = 0
		self.area = 0
		# Maybe use something like leds["midpoint"], aka a dictionary

		# TODO: Put following into settings file

		self.DEBUG = debug

		# For X, Y, and Z margin of error
		self.X_MOE = 10 # pixels
		self.Y_MOE = 10 # pixels
		self.TWIST_MOE = math.pi / 8 # should be in radians

		#self.LED_COLOR_LOWER = np.array ([50, 75, 220]) # green with a narrow value range to pick up leds only
		#self.LED_COLOR_UPPER = np.array ([80, 255, 255])

		self.LED_COLOR_LOWER = np.array ([160, 75, 90]) # red 
		self.LED_COLOR_UPPER = np.array ([179, 255, 255])


		# For Z-Axis Direction Determination
		self.MAX_AREA = 100000

		# For adaptiveThreshold
		self.BLOCKSIZE = 11
		self.C = 1

	def update_image (self, src_image):
		self.images["Src"] = src_image

	def find_base (self):
		self.process_image ()
		if self.LEDS_FOUND:
			print "LEDS_FOUND!"
			self.process_data ()
			self.update_instructions ()
		else:
			self.null_instructions ()
	
		self.send_instuctions ()

		if self.DEBUG:
			self.screen_update ()
			self.print_results ()

	def process_image (self):
		self.images["HSV_Mask"] = cv2.cvtColor (self.images["Src"], cv2.COLOR_BGR2HSV) # Expensive command

		self.images["Color_Mask"] = cv2.inRange (self.images["HSV_Mask"], self.LED_COLOR_LOWER, self.LED_COLOR_UPPER)

		self.images["Blur"] = cv2.blur (self.images["Color_Mask"], (9, 9)) 

		self.images["Dilate"] = cv2.dilate (self.images["Blur"], None, iterations=21)
		self.images["Dilate_Output"] = deepcopy (self.images["Dilate"]) # Since cv2.adaptiveThreshold modifies the src image

		# Detects lines
		self.images["Thresh"] = cv2.adaptiveThreshold (self.images["Dilate"], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, self.BLOCKSIZE, self.C)

		# Finds contours of lines
		contours, heirarchy = cv2.findContours (self.images["Dilate"], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)		 

		self.led_pos = []
		for contour in contours:
			self.led_pos.append (cv2.minEnclosingCircle (contour)[0]) # Index 0 for minEnclosingCircle returns the center
			#radius.append (cv2.minEnclosingCircle (contour)[1]) # Can be used for error checking
	
		if len (self.led_pos) == 3:
			self.LEDS_FOUND = True
		else:
			self.LEDS_FOUND = False

	def process_data (self):
		# Need to convert array of point tuples to array of pts
		self.led_pts = []
		for led in self.led_pos:
			self.led_pts.append (pt (led[0], led[1]))
		
		self.base_tri = tri (self.led_pts[0], self.led_pts[1], self.led_pts[2])

		self.hypotenuse = self.base_tri.hypotenuse ()

		self.midpoint = self.hypotenuse.midpoint ()
		
		self.offset_from_base = pt (self.midpoint.x - (self.COLS / 2), self.midpoint.y - (self.ROWS / 2))

		#self.twist = self.base_tri.adjacent_angle (self.midpoint)
		self.twist = math.atan2 (self.midpoint.y, self.midpoint.x)
		print self.twist

		self.opposite_pt = self.base_tri.opposite_pt ()

	def update_instructions (self):
		# Z
		# TODO: Also consider implementing fuzzy logic here
		self.area = self.base_tri.area ()
		
		if self.area < self.MAX_AREA:
			self.Instructions.Z = -1
		else:
			self.Instructions.Z = 0

		# X and Y
		# TODO: Consider implementing fuzzy logic here then passing a velocity value between 0 and 1
		if self.offset_from_base.x < -self.X_MOE and self.offset_from_base.y < -self.Y_MOE: # top left
			self.Instructions.X = -1
			self.Instructions.Y = 1
		elif self.offset_from_base.x > self.X_MOE and self.offset_from_base.y < -self.Y_MOE: # top right
			self.Instructions.X = 1
			self.Instructions.Y = 1
		elif self.offset_from_base.x < -self.X_MOE and self.offset_from_base.y > self.Y_MOE: # bottom left
			self.Instructions.X = -1
			self.Instructions.Y = -1
		elif self.offset_from_base.x > self.X_MOE and self.offset_from_base.y > self.Y_MOE: # bottom right
			self.Instructions.X = 1
			self.Instructions.Y = -1
		else:
			self.Instructions.X = 0
			self.Instructions.Y = 0

		# Twist
		#
		#adds 1/8pi to twist to account for base and outputs
		#clockwise if in upper quadrant and
		#counter-clockwise if in lower quadrant
		#
		# TODO: Use math.atan2 (y, x)
		adjustment = (math.pi / 8)
		if self.twist > (math.pi - adjustment + self.TWIST_MOE) and (self.twist) < ((math.pi * 2) - adjustment - self.TWIST_MOE):
			self.Instructions.Twist = 1
		elif self.twist > ((math.pi * 2) - adjustment + self.TWIST_MOE) and self.twist < 0:
			self.Instructions.Twist = -1
		elif self.twist < (math.pi - adjustment - self.TWIST_MOE):
			self.Instructions.Twist = -1
		else: 
			self.Instructions.Twist = 0

	def send_instuctions (self):
		# TODO: Add ROS publisher
		# TODO: Publish using proto2.Flight_Controls
		print "====Instructions Published!===="

	def	screen_update (self):
		if self.LEDS_FOUND:
			cv2.line (self.image, (int (self.midpoint.x), int (self.midpoint.y)), (int (self.opposite_pt.x), int (self.opposite_pt.y)), (0,0,0))

			cv2.circle (self.image, (int (self.midpoint.x), int (self.midpoint.y)), 5, (0, 0, 0))
			cv2.circle (self.image, (int (self.COLS / 2), int (self.ROWS / 2)), int (self.X_MOE / 2), (0, 0, 0))

			for pt in self.led_pts:
				cv2.circle (self.image, (int (pt.x), int (pt.y)), 10, (0, 0, 0))

		cv2.imshow ("self.image", self.image)
		cv2.imshow ("self.dilated_image", self.dilated_image)

	def print_results (self):
		print "Return: " + str (self.Instructions.Return)
		print "X: " + str (self.Instructions.X)
		print "Y: " + str (self.Instructions.Y)
		print "Z: " + str (self.Instructions.Z)
		print "Twist: " + str (self.Instructions.Twist)
		print

	def null_instructions (self):
		self.Instructions.Return = 0
		self.Instructions.X = 0
		self.Instructions.Y = 0
		self.Instructions.Z = 0
		self.Instructions.Twist = 0
	
def main ():
	cap = cv2.VideoCapture (0)

	vision = Base_Tracker (cap, debug=1)

	while cap.isOpened ():
		ret, image = cap.read ()
		vision.update_image (image)
		vision.find_base () 

		key = cv2.waitKey (20) # refresh rate is 20 milliseconds
		if key == 1048603 or key == 27: # exit on ESC
			cv2.destroyAllWindows ()
			cap.release ()

if __name__=="__main__":
	profile.run ("main ()")
