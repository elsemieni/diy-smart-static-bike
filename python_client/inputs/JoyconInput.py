from pyjoycon import JoyCon, get_L_id, get_R_id

"""
Class used for reading values from JoyCon controllers 
"""


class JoyconInput:
    ERROR_MESSAGE = "No Joy-cons detected. Are any of them connected via bluetooth?"

    def __init(self):
        self.joycon_id1 = get_L_id()
        self.joycon_id2 = get_R_id()
        self.joycon = None

    '''
    Initializes the input.
    Return True or False if it was sucessful or not
    '''

    def initialize(self):
        try:
            self.joycon = JoyCon(*self.joycon_id1)
            print("JoyCon L detected")
        except:
            try:
                self.joycon = JoyCon(*self.joycon_id2)
                print("JoyCon R detected")
            except:
                print("No Joy-cons detected")
                return False
        return True

    '''
    Read the raw value of your device. Please return it in float format. 
    Parameter is "X", "Y" or "Z"
    I don't care about max/min values,
    the program will take that in callibration process
    '''

    def read(self, axis):
        return self.joycon.get_status()["gyro"][axis]

    '''
    Shutdown/deinitalize the input device
    Called when closing the program
    '''

    def shutdown(self):
        pass
