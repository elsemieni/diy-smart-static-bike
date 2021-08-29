"""
Place holder
"""

import _thread
from flask import Flask
from flask_socketio import SocketIO
from netifaces import interfaces, ifaddresses, AF_INET
import PySimpleGUI as sg
import json


class AndroidInput:
    ERROR_MESSAGE = "Perhaps some sort of error when creating Socket Server.\nMaybe restarting application might work"

    def __init(self):
        pass

    '''
    Initializes the input.
    Return True or False if it was sucessful or not
    '''

    def initialize(self):
        self.app = Flask("Poor man smart cycle Web Client")
        self.socket_ = SocketIO(self.app)
        self.coords = None

        @self.app.route('/')
        def index():
            return ""

        @self.socket_.on('onCoords')
        def onCoords(message):
            print(message)
            tempcoords = json.loads(message)
            self.coords = {"x": tempcoords[0], "y": tempcoords[1], "z": tempcoords[2]}

        ips = []
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'null'}])]
            if addresses[0] != "null":
                ips.append(addresses[0])

        message = "Connect your phone to your Wifi, Install/execute app (gyroscope) and try to enter to one of these " \
                  "addresses: "
        for i in ips:
            message += "\nhttp://" + i + ":5000/"
        message += "\n\nPress connect only after you click Ok on this message"
        sg.popup(message)

        def flaskThread():
            self.socket_.run(self.app, host="0.0.0.0")

        _thread.start_new_thread(flaskThread, ())

        return True

    '''
    Read the raw value of your device. Please return it in float format. 
    Parameter is "X", "Y" or "Z"
    I don't care about max/min values,
    the program will take that in callibration process
    '''

    def read(self, axis):
        if self.coords is not None:
            return self.coords[axis]
        else:
            return 0.0

    '''
    Shutdown/deinitalize the input device
    Called when closing the program
    '''

    def shutdown(self):
        pass
