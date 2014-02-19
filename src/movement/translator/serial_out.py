import os
import sys
from time import sleep

#import Adafruit_BBIO.UART as UART
import serial

sys.path.append (os.path.abspath("../../"))
from communication.zmq_communicator import communicator

ser = serial.Serial (port = "/dev/ttyACM0", baudrate=9600)

def setup_serial ():
    ser.close ()
    ser.open ()

def send_flight_controls (pitch, yaw, roll, z, arm, hover):
    if ser.isOpen ():
        ser.write ("B{p},{y},{r},{z_pos},{a},{h}\n".format (p=int (pitch), y=int (yaw), r=int (roll), z_pos=int (z), a=int (arm), h=int (hover)))
        print "B{p},{y},{r},{z_pos},{a},{h}\n".format (p=int (pitch), y=int (yaw), r=int (roll), z_pos=int (z), a=int (arm), h=int (hover))

def main ():
    com = communicator ("Translator")
    last_timestamp = 0

    while True:
        msg = {"message":0, "time":0}
        msg = com.get_message ("Switcher")
        #print msg
        if msg and msg["time"] > last_timestamp:
            last_timestamp = msg["time"]
    
            pitch = msg["message"]["Pitch"] * 100
            yaw = msg["message"]["Yaw"] * 100
            roll = msg["message"]["Roll"] * 100
            z = msg["message"]["Z"] * 100
            arm = int (msg["message"]["Arm"]) 
            hover = int (msg["message"]["Hover"])

            send_flight_controls (pitch, yaw, roll, z, arm, hover)
        sleep (.05)

if __name__=="__main__":
    setup_serial ()
    main ()
