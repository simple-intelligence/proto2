import subprocess
import sys
import threading
from time import sleep

class Controller:
    class Parser (threading.Thread):
        def __init__(self, _xboxdrv_process):
            """
            Parser parses the input from xboxdrv. It runs as a seperate thread to prevent
            stale data when get_values() is called
            """
            threading.Thread.__init__(self)
        
            self.xboxdrv = _xboxdrv_process
            self.control_inputs = {}

        def run (self):
            while True:
                line = self.xboxdrv.stdout.readline ()

                try:
                    """
                    This is a somewhat hackey method but it should work for all controllers that xboxdrv can handle.
                    
                    xboxdrv prints off controller inputs as "X1:120 Y1: 10 select:1" etc...
                    Just splitting by spaces does not work as it would seperate "Y1:" and "10". 
                    This method removes all spaces after a ":" but does not affect the spaces after the numerical
                    value of an input.
                    """
                    line = line.replace (":      ", ":     ")
                    line = line.replace (":     ",  ":    ")
                    line = line.replace (":    ",   ":   ")
                    line = line.replace (":   ",    ":  ")
                    line = line.replace (":  ",     ": ")
                    line = line.replace (": ",      ":")

                    # Sometimes there's two spaces a value; replace with one
                    line = line.replace ("  ", " ")

                    entries = line.split (" ")

                    self.control_inputs = {}
                    for entry in entries:
                        s = entry.split (":")
                        self.control_inputs[str (s[0])] = int (s[-1])

                # Catches controller info that xboxdrv outputs at the beginning
                except ValueError:
                    pass

    def __init__(self, return_values=None, return_as=None, in_range=None, out_range=None):
        """
        Controller() is a class for getting input values from an xbox/playstation or other controller
        recognized by the program xboxdrv. By default Controller returns values for every button on the 
        controller as a dictionary.

        Optional Parameters:
        return_values is an optional list of the values to return from the controller. use get_input_names()
            to get the names of these values.
        return_as is an optional list of names to return the input values as. it must be the same length 
            as return_values
        in_range is an optional tuple in the format (min, max) where min is the lowest incoming value and max
            the greatest
        out_range is an optional tuple in the format (min, max) where min is the lowest desired outgoing value and max
            the greatest

        Note:
        return_values may be present while return_as can still be none, however, in_range and out_range must both exist
        """
        if return_values and return_as:
            if not len (return_values) == len (return_as):
                sys.exit ("return_values and return_as must be the same length!")
        elif return_as and not return_values:
                sys.exit ("No values to return!")

        if not in_range and not out_range:
            pass
        elif len (in_range) !=2 or len (out_range) != 2:
            sys.exit ("in_range and out_range must be in format: (min, max)")
        
        self._in_range = in_range
        self._out_range = out_range
            
        self._return_values = return_values
        self._return_as = return_as

        controller = subprocess.Popen (["sudo", "xboxdrv", "-d"], stdout=subprocess.PIPE)

        # This waits for password input
        sleep (2)

        self.line_parser = self.Parser (controller)
        self.line_parser.daemon = True
        self.line_parser.start ()

        self.outputs = {}

    def map_range (self, x, in_min, in_max, out_min, out_max):
        """
        map_range() maps the inputs values ranging from in_min to in_max to output values
        ranging from out_min to out_max. This can handle both negative and positive
        min and max values
        """
        x = float (x)
        in_min = float (in_min)
        in_max = float (in_max)
        out_min = float (out_min)
        out_max = float (out_max)
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def get_input_names (self):
        """
        get_input_names() returns a list of the names of all the values coming from xboxdrv.
        """
        #TODO: this could fail if the parser catches a line from the info text that xboxdrv puts out
        while not self.line_parser.control_inputs:
            pass

        names = []
        for key in self.line_parser.control_inputs.keys ():
            names.append (key)
        return names 

    def get_values (self):
        """
        get_values() returns the values specified by the caller or 
        all the values if no values specified
        """
        self.outputs = {}

        # Changes return values names to specified names
        if self._return_values and self._return_as:
            try:
                for key in range (len (self._return_values)):
                    self.outputs [str (self._return_as[key])] = self.line_parser.control_inputs[self._return_values[key]]
            except KeyError:
                pass

        # Does not change names but does only return specified value
        elif self._return_values and not self._return_as:
            try:
                for key in range (len (self._return_values)):
                    self.outputs [str (self._return_values[key])] = self.line_parser.control_inputs[self._return_values[key]]
            except KeyError:
                pass

        else:
            self.outputs = self.line_parser.control_inputs

        # Maps values to a range
        if self._in_range and self._out_range:
            for key in self.outputs:
                self.outputs[key] = self.map_range (self.outputs[key], self._in_range[0], self._in_range[1], self._out_range[0], self._out_range[1])

        return self.outputs
