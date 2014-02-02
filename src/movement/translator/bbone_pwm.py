import os
import sys
import time

#import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

sys.path.append (os.path.abspath("../../"))
from communication.zmq_communicator import communicator

# Pins
pitch = "P9_14"
roll = "P9_16"
yaw = "P8_19"
z = "P8_13"

def setup ():
	PWM.start (pitch, 0, frequency=50) 
	PWM.start (roll, 0, frequency=50) 
	PWM.start (yaw, 0, frequency=50) 
	PWM.start (z, 0, frequency=50) 

	i = 0
	while True:
		PWM.set_duty_cycle (pitch, i)
		PWM.set_duty_cycle (roll, i)
		PWM.set_duty_cycle (yaw, i)
		PWM.set_duty_cycle (z, i)
		if i == 100:
			i = 0
		else:
			i += 1
		time.sleep (.02)

def main ():
	com = communicator ("Translator")

	while True:
		msg = com.get_message ("Direction")
		if msg:
			pitch = msg["message"]["Pitch"] * 100
			yaw = msg["message"]["Yaw"] * 100
			roll = msg["message"]["Roll"] * 100
			z = msg["message"]["Z"] * 100
			print pitch
			print yaw
			print roll
			print z
		time.sleep (.5)
	
if __name__=="__main__":
	setup ()
