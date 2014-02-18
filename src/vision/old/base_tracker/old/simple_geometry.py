import math
import numpy as np

class directions:
	def __init__(self):
		self.Return = 0
		self.X = 0
		self.Y = 0
		self.Z = 0
		self.Twist = 0


class pt:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(%s, %s)" % (self.x, self.y)
	def __repr__(self):
		return "(%s, %s)" % (self.x, self.y)


class line:
	def __init__(self, p1, p2):
		self.pt1 = p1
		self.pt2 = p2

	def length(self):
		return np.sqrt(pow(self.pt1.x - self.pt2.x, 2) + pow(self.pt1.y - self.pt2.y, 2))

	def midpoint(self):
		return pt (((self.pt1.x + self.pt2.x) / 2), ((self.pt1.y + self.pt2.y) / 2))

	def slope(self):
		if self.pt2.x - self.pt1.x != 0:
			return math.atan((self.pt2.y - self.pt1.y) / (self.pt2.x - self.pt1.x))
		else:
			return math.atan(0)

class tri:
	def __init__(self, p1, p2, p3):
		self.pt1 = p1
		self.pt2 = p2
		self.pt3 = p3
		self.l1 = line (p1, p2)
		self.l2 = line (p2, p3)
		self.l3 = line (p1, p3)
		self.iter_tri = [self.l1, self.l2, self.l3]

	def hypotenuse(self):
		line_lengths = []
		for line in self.iter_tri:
			line_lengths.append (line.length())

		longest = max (line_lengths)

		if line_lengths.index (longest) == 0:
			return self.l1
		if line_lengths.index (longest) == 1:
			return self.l2
		if line_lengths.index (longest) == 2:
			return self.l3

	def area(self):
		s = (self.l1.length() + self.l2.length() + self.l3.length()) / 2
		return np.sqrt(s * (s - self.l1.length()) * (s - self.l2.length()) * (s - self.l3.length()))

	def opposite_pt(self):
		line_lengths = []
		for line in self.iter_tri:
			line_lengths.append (line.length())

		longest = max (line_lengths)

		if line_lengths.index (longest) == 0:
			return self.pt3
		if line_lengths.index (longest) == 1:
			return self.pt1
		if line_lengths.index (longest) == 2:
			return self.pt2

	def adjacent_angle(self, midpoint):
		"""
		finds the opposite pt and angle between it and midpoint of triangle
		returns between 0 and 2pi
		"""
		opposite_pt = self.opposite_pt()
		if opposite_pt.x > midpoint.x and opposite_pt.y < midpoint.y:
			return line(opposite_pt, midpoint).slope()
		elif opposite_pt.x < midpoint.x and opposite_pt.y < midpoint.y:
			return math.pi - line(opposite_pt, midpoint).slope()
		elif opposite_pt.x < midpoint.x and opposite_pt.y > midpoint.y:
			return -line(opposite_pt, midpoint).slope() + math.pi
		elif opposite_pt.x > midpoint.x and opposite_pt.y > midpoint.y:
			return 2 * math.pi - line(opposite_pt, midpoint).slope()
		else:
			return 0
