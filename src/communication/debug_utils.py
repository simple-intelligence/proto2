import sys
import json

try:
	settings = json.load (open ("/home/dustin/programming/ros_workspace/src/proto2/Global_Settings.json", "r"))
except:
	sys.stderr.write ("Global_Settings.json does not exist or is not in json format!\n")
	sys.exit ()

def print_d (msg):
	if settings["Debug"]:
		sys.stderr.write (str (msg) + "\n")
