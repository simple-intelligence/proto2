import zmq
import time

context = zmq.Context ()

socket = context.socket (zmq.PUB)

socket.bind ("tcp://192.168.0.13:5000")

num_messages = 0
while True:
	socket.send ("Hello Dustin's Pi! {num}".format (num=num_messages))
	print "Hello Dustin's Pi! {num}".format (num=num_messages)
	num_messages += 1
	time.sleep (1)

