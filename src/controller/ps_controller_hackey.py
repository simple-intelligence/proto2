import sys
import os
import threading
from time import sleep

sys.path.append (os.path.abspath("../"))
from communication.zmq_communicator import communicator

final_packet = {"Pitch":0, "Yaw":0, "Roll":0, "Z":0, "Arm":0}
com = communicator ("Controller")

class msg_passer (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run (self):
		while True:
			try:
				com.send_message (final_packet)
				print final_packet
			except:
				pass
			sleep (1)

IS_ARMED = 0

passer = msg_passer ()
passer.daemon = True
passer.start ()

while True:
	controls = sys.stdin.readline ()


	x1 = controls[0:6]
	y1 = controls[7:13]
	x2 = controls[15:21]
	y2 = controls[22:28]
	arm = controls[93:99]
	unarm = controls[112:118]

	try:
		control_out = {}
		for i in (x1, y1, x2, y2, arm, unarm):
			s = i.split (":")
			control_out[s[0]] = int (s[1])
	except ValueError:
		pass
	except IndexError:
		pass
	except KeyError:
		pass

	try:
		control_out['Y1'] = 255 - control_out['Y1']
		control_out['Y2'] = 255 - control_out['Y2']

		for i in control_out.keys ():
			control_out[i] = (control_out[i] / 255.0) - 0.5
			if control_out[i] < .15 and control_out[i] > -.15: control_out[i] = 0


		final_packet = {"Pitch":control_out["Y2"], "Yaw":control_out["X1"], "Roll":control_out["X2"], "Z":control_out["Y1"], "Arm":0}

		final_packet["Arm"] = IS_ARMED

		if IS_ARMED:
			if control_out['[]'] > 0: 
				final_packet["Arm"] = 0
				IS_ARMED = 0
		if not IS_ARMED:
			if control_out['/\\'] > 0: 
				final_packet["Arm"] = 1
				IS_ARMED = 1

		#print final_packet
		com.send_message (final_packet)

	except KeyError:
		pass
