import os
import sys
import time

import Adafruit_BBIO.UART as UART
import serial

sys.path.append (os.path.abspath("../../"))
from communication.zmq_communicator import communicator

def setup ():
	UART.setup ("UART1")
	global ser = serial.Serial (port = "/dev/tty01", baudrate=9600)
	ser.close ()
	ser.open ()

def send_flight_controls (pitch, yaw, roll, z):
	if ser.isOpen ():
		ser.write ("{p} {y} {r} {z}".format (pitch, yaw, roll z))
	

def main ():
	com = communicator ("Translator")
	last_timestamp = 0

	while True:
		msg = com.get_message ("Direction")
		if msg["time"] > last_timestamp:
			last_timestamp = msg["time"]
	
			pitch = msg["message"]["Pitch"] * 100
			yaw = msg["message"]["Yaw"] * 100
			roll = msg["message"]["Roll"] * 100
			z = msg["message"]["Z"] * 100

			send_flight_controls (pitch, yaw, roll z)

if __name__=="__main__":
	main ()
