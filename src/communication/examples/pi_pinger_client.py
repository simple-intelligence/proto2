import zmq
import time

debug = True

context = zmq.Context ()

socket = context.socket (zmq.SUB)

if debug:
	print "Connecting to socket!"
socket.connect ("tcp://192.168.0.13:5000")
if debug:
	print "Conneced to socket!"
socket.setsockopt (zmq.SUBSCRIBE, "")

connected = 0
num_pings = 0
prev_msg_num = 0
disconnection_timer = 0
msg = "Init Message -10"
while True:
	prev_msg_num = int (msg.split ()[-1])
	msg = socket.recv ()
	if debug:
		print msg
	if int (msg.split ()[-1]) - 1 == int (prev_msg_num):
		num_pings += 1
		if num_pings == 5:
			connected = True
		if connected:
			if debug:
				print "Connected!"
			disconnection_timer = 0
	else:
		num_pings = 0
		connected = False
		disconnection_timer += 1
		if disconnection_timer > 5:
			print "Disconnected!"
			
	
