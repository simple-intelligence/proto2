import sys
import os
import threading
from time import sleep
from xboxdrv_parser import Controller

sys.path.append (os.path.abspath("../"))
from communication.zmq_communicator import communicator

def adjust_throttle (inputs):
    THROTTLE_C = .26
    inputs["Z"] = inputs["Z"] + (THROTTLE_C * (abs (inputs["Pitch"]) + abs (inputs["Roll"])))
    return inputs

def main ():
    com = communicator ("Controller")

    final_packet = {"Pitch":0, "Yaw":0, "Roll":0, "Z":0, "Arm":0, "Hover":0}

    controller =  Controller (["X1", "Y1", "X2", "Y2", "[]", "/\\", "X", "O", "R2", "L2"], ["Yaw", "Z", "Roll", "Pitch", "Unarm", "Arm", "Altitude_Helper", "Altitude_Helper_Off", "Hover1", "Hover2"])

    IS_ARMED = 0
    IS_ALTITUDE_HELPED = 0

    while True:
        inputs = controller.get_values ()

        try:
            """
            inputs["Yaw"] = controller.map_range (inputs["Yaw"], 0, 255, 0.25, -0.25)
            inputs["Pitch"] = controller.map_range (inputs["Pitch"], 0, 255, -0.25, 0.25)
            inputs["Z"] = controller.map_range (inputs["Z"], 0, 255, 0.0, 0.5)
            inputs["Roll"] = controller.map_range (inputs["Roll"], 0, 255, -0.5, 0.5)

            inputs["Arm"] = controller.map_range (inputs["Arm"], 0, 255, 0.0, 1.0)
            inputs["Unarm"] = controller.map_range (inputs["Unarm"], 0, 255, 0.0, 1.0)
            inputs["Altitude_Helper"] = controller.map_range (inputs["Altitude_Helper"],0, 255, 0.0, 1.0)
            inputs["Altitude_Helper_Off"] = controller.map_range (inputs["Altitude_Helper_Off"], 0, 255, 0.0, 1.0)
            """

            # Massaging values
            for i in inputs.keys ():
                inputs[i] = inputs[i] / 255.0 

            # Throttle should start at 0
            inputs["Z"] = 1 - inputs["Z"]

            # Stick values should be centered around 0
            inputs["Pitch"] = inputs["Pitch"] - 0.5
            inputs["Yaw"] = inputs["Yaw"] - 0.5
            inputs["Roll"] = inputs["Roll"] - 0.5

            # Reversing
            inputs["Yaw"] = -inputs ["Yaw"]
            
            # Sticks scaled down
            inputs["Z"] = inputs["Z"] / 2
            inputs["Pitch"] = inputs["Pitch"] / 2
            inputs["Yaw"] = inputs["Yaw"] / 2
            inputs["Roll"] = inputs["Roll"] / 2

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

            if inputs["Hover1"] == 1.0:
                inputs["Hover1"] = 1.0
            else:
                inputs["Hover1"] = 0
            
            if inputs["Hover2"] == 1.0:
                inputs["Hover2"] = 1.0
            else:
                inputs["Hover2"] = 0

            if inputs["Hover1"] and inputs["Hover2"]:
                IS_HOVER = 1
            else:
                IS_HOVER = 0

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

            final_packet = {"Pitch":inputs["Pitch"], "Yaw":inputs["Yaw"], "Roll":inputs["Roll"], "Z":inputs["Z"], "Arm":IS_ARMED, "Hover":IS_HOVER}

            # Clips small controller movements to zero. Necessary especially for throttle so copter will arm
            for key in final_packet.keys ():
                if abs (final_packet[key]) < .025:
                    final_packet[key] = 0.0 
        
            com.send_message (final_packet)

        except KeyError:
            pass

        print final_packet
    
        # Send 5 commands/sec
        sleep (.2)


main ()
