"""
This is a custom class for read from any device you want!
Just complete this class as you wish and you re up to go!
"""


class CustomInput:
    ERROR_MESSAGE = "Custom error message if it fails to initialize"

    def __init(self):
        pass

    '''
    Initializes the input.
    Return True or False if it was sucessful or not
    '''

    def initialize(self):
        return True

    '''
    Read the raw value of your device. Please return it in float format. 
    Parameter is "X", "Y" or "Z"
    I don't care about max/min values,
    the program will take that in callibration process
    '''

    def read(self, axis):
        return 0.0

    '''
    Shutdown/deinitalize the input device
    Called when closing the program
    '''

    def shutdown(self):
        pass
