import subprocess
import sys
import threading
from time import sleep

class Controller:
    class Parser (threading.Thread):
        def __init__(self, _xboxdrv_process):
            threading.Thread.__init__(self)
        
            self.xboxdrv = _xboxdrv_process
            self.control_inputs = {}

        def run (self):
            while True:
                line = self.xboxdrv.stdout.readline ()

                try:
                    # This is a somewhat hackey method but it should work for all controllers that xboxdrv can handle
                    line = line.replace (":      ", ":     ")
                    line = line.replace (":     ",  ":    ")
                    line = line.replace (":    ",   ":   ")
                    line = line.replace (":   ",    ":  ")
                    line = line.replace (":  ",     ": ")
                    line = line.replace (": ",      ":")

                    line = line.replace ("  ", " ")

                    entries = line.split (" ")

                    self.control_inputs = {}
                    for entry in entries:
                        s = entry.split (":")
                        self.control_inputs[str (s[0])] = int (s[-1])

                # Catches controller info that xboxdrv outputs at the beginning
                except ValueError:
                    pass

    def __init__(self, _return_values=None, _return_as=None):
        if _return_values and _return_as:
            if not len (_return_values) == len (_return_as):
                sys.exit ("return_values and return_as must be the same length!")
        elif _return_as and not _return_values:
                sys.exit ("Nothing to return!")
            
        self.return_values = _return_values
        self.return_as = _return_as

        controller = subprocess.Popen (["sudo", "xboxdrv", "-d"], stdout=subprocess.PIPE)

        # This waits for password input
        sleep (2)

        self.line_parser = self.Parser (controller)
        self.line_parser.daemon = True
        self.line_parser.start ()

        self.outputs = {}

    def get_input_names (self):
        while not self.line_parser.control_inputs:
            pass

        names = []
        for key in self.line_parser.control_inputs.keys ():
            names.append (key)
        return names 

    def get_values (self):
        self.outputs = {}
        if self.return_values and self.return_as:
            try:
                for key in range (len (self.return_values)):
                    self.outputs [str (self.return_as[key])] = self.line_parser.control_inputs[self.return_values[key]]
            except KeyError:
                pass
            return self.outputs
        elif self.return_values and not self.return_as:
            try:
                for key in range (len (self.return_values)):
                    self.outputs [str (self.return_values[key])] = self.line_parser.control_inputs[self.return_values[key]]
            except KeyError:
                pass
            return self.outputs
        else:
            return self.line_parser.control_inputs
        
def main ():
    #ps3 = Controller (["Y1", "Y2", "X1", "X2"])
    ps3 = Controller (["Y1", "Y2", "X1", "X2"], ["A", "B", "C", "D"])
    #ps3 = Controller (["Y1", "Y2", "X1", "X2"], ["B", "C", "D"])

    print ps3.get_input_names ()
    
    while True:
        print ps3.get_values ()
        sleep (.25)

main ()

"""
controller = subprocess.Popen (["sudo", "xboxdrv", "-d"], stdout=subprocess.PIPE)

while True:
    line = controller.stdout.readline ()

    try:
        line = line.replace  (":      ", ":     ")  
        line = line.replace (":     ",  ":    ")    
        line = line.replace (":    ",   ":   ") 
        line = line.replace (":   ",    ":  ")  
        line = line.replace (":  ",     ": ")
        line = line.replace (": ",      ":")

        line = line.replace ("  ", " ")

        entries = line.split (" ")

        control_inputs = {}
        for entry in entries:
            s = entry.split (":")
            control_inputs[str (s[0])] = int (s[-1])

        print control_inputs
    except ValueError:
        pass
        
"""
"""Proof of concept and kinda-sorta-hackey algorithm
src = "X1:131 Y1:120  X2:137 Y2:121  du:  0 dd:  0 dl:  0 dr:  0  select:0 ps:0 start:0  L3:0 R3:0  /\:  0 O:  0 X:  0 []:  0  L1:142 R1:  0  L2:  0 R2:  0"

line = src.replace  (":      ", ":     ")   
line = line.replace (":     ",  ":    ")    
line = line.replace (":    ",   ":   ") 
line = line.replace (":   ",    ":  ")  
line = line.replace (":  ",     ": ")
line = line.replace (": ",      ":")

line = line.replace ("  ", " ")

entries = line.split (" ")

control_inputs = {}
for entry in entries:
    s = entry.split (":")
    control_inputs[str (s[0])] = int (s[-1])

print src
print
print line
print
print entries
print
print control_inputs
"""
