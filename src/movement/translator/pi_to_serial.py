import os
import sys
from time import sleep

#import Adafruit_BBIO.UART as UART
import serial

sys.path.append (os.path.abspath("../../"))
from communication.zmq_communicator import communicator

ser = serial.Serial (port = "/dev/ttyACM1", baudrate=9600)

def setup_serial ():
	ser.close ()
	ser.open ()

def send_flight_controls (pitch, yaw, roll, z, arm):
	if ser.isOpen ():
		ser.write ("{p},{y},{r},{z_pos},{a}\n".format (p=int (pitch), y=int (yaw), r=int (roll), z_pos=int (z), a=int (arm)))
		print "{p},{y},{r},{z_pos},{a}\n".format (p=int (pitch), y=int (yaw), r=int (roll), z_pos=int (z), a=int (arm))

def main ():
	com = communicator ("Translator")
	last_timestamp = 0

	while True:
		msg = {"message":0, "time":0}
		msg = com.get_message ("Direction")
		#print msg
		if msg and msg["time"] > last_timestamp:
			last_timestamp = msg["time"]
	
			pitch = msg["message"]["Pitch"] * 100
			yaw = msg["message"]["Yaw"] * 100
			roll = msg["message"]["Roll"] * 100
			z = msg["message"]["Z"] * 100
			arm = int (msg["message"]["Arm"]) 

			send_flight_controls (pitch, yaw, roll, z, arm)
		sleep (.05)

if __name__=="__main__":
	setup_serial ()
	main ()
