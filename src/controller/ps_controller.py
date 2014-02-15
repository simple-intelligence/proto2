import sys
import os
import threading
from time import sleep
from xboxdrv_parser import Controller

sys.path.append (os.path.abspath("../"))
from communication.zmq_communicator import communicator

def adjust_throttle (inputs):
    THROTTLE_C = .26 # This is some constant that multiplies abs (yaw) + abs (pitch) for the throttle helper
    inputs["Z"] = inputs["Z"] + (THROTTLE_C * (abs (inputs["Pitch"]) + abs (inputs["Roll"])))
    return inputs

def map_input (inputs, binary=False):
    return 

def main ():
    com = communicator ("Controller")

    final_packet = {"Pitch":0, "Yaw":0, "Roll":0, "Z":0, "Arm":0}

    controller =  Controller (["X1", "Y1", "X2", "Y2", "[]", "/\\", "X", "O"], ["Yaw", "Z", "Roll", "Pitch", "Unarm", "Arm", "Altitude_Helper", "Altitude_Helper_Off"])

    IS_ARMED = 0
    IS_ALTITUDE_HELPED = 0

    while True:
        inputs = controller.get_values ()

        try:
            # TODO: Just write a map function for this...

            # Massaging values
            for i in inputs.keys ():
                inputs[i] = inputs[i] / 255.0 

            # Throttle should start at 0
            inputs["Z"] = 1 - inputs["Z"]

            # Stick values should be centered around 0
            inputs["Pitch"] = inputs["Pitch"] - 0.5
            inputs["Yaw"] = inputs["Yaw"] - 0.5
            inputs["Roll"] = inputs["Roll"] - 0.5

            # Have to press hard to prevent accidental arm/unarm/throttle helper/throttle hold
            if inputs["Unarm"] == 1.0:
                inputs["Unarm"] = 1.0
            else:
                inputs["Unarm"] = 0

            if inputs["Arm"] == 1.0:
                inputs["Arm"] = 1.0
            else:
                inputs["Arm"] = 0

            if inputs["Altitude_Helper"] == 1.0:
                inputs["Altitude_Helper"] = 1.0
            else:
                inputs["Altitude_Helper"] = 0
            
            if inputs["Altitude_Helper_Off"] == 1.0:
                inputs["Altitude_Helper_Off"] = 1.0
            else:
                inputs["Altitude_Helper_Off"] = 0

            # Reversing
            inputs["Yaw"] = -inputs ["Yaw"]
            
            # Sticks scaled down
            inputs["Z"] = inputs["Z"] / 2
            inputs["Pitch"] = inputs["Pitch"] / 2
            inputs["Yaw"] = inputs["Yaw"] / 2
            inputs["Roll"] = inputs["Roll"] / 2

            # Logic so you don't have to hold arm/unarm/throttle_helper/etc
            if IS_ARMED and inputs["Unarm"]:
                inputs["Arm"] = 0
                IS_ARMED = 0
                print "UNARMED!" 
            if not IS_ARMED and inputs["Arm"]:
                inputs["Arm"] = 1
                IS_ARMED = 1
                print "ARMED!"

            if IS_ALTITUDE_HELPED and inputs["Altitude_Helper_Off"]:
                IS_ALTITUDE_HELPED = 0
                print "Altitude Helper OFF!"
            if not IS_ALTITUDE_HELPED and inputs["Altitude_Helper"]:
                IS_ALTITUDE_HELPED = 1
                print "Altitude Helper ON!"

            # Altitude Adjust 
            if IS_ALTITUDE_HELPED:
                inputs = adjust_throttle (inputs)

            final_packet = {"Pitch":inputs["Pitch"], "Yaw":inputs["Yaw"], "Roll":inputs["Roll"], "Z":inputs["Z"], "Arm":IS_ARMED}

            for key in final_packet.keys ():
                if final_packet[key] < 0.025 and final_packet[key] > -0.025:
                    final_packet[key] = 0.0 
        
            com.send_message (final_packet)

        except KeyError:
            pass

        print final_packet
    
        sleep (.2)


main ()
