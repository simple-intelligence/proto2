import sys
import json

class debugging:
	def __init__(self):
		try:
			self.settings = json.load (open ("/home/dustin/programming/ros_workspace/src/proto2/Global_Settings.json", "r"))
		except:
			sys.stderr.write ("Global_Settings.json does not exist or is not in json format!\n")
			sys.exit ()

		if self.settings["Debug"]:
			print "DEBUG = True"

	def print_d (self, msg):
		if self.settings["Debug"]:
			sys.stderr.write (str (msg) + "\n")
			print str (msg)
