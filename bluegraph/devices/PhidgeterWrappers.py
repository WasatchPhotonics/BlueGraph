""" Simulation devices for bluegraph visualizations
"""

import time
import numpy
import random
import logging
import Queue
import multiprocessing

from collections import deque

from bluegraph.devices import Simulation

from phidgeter.temperature import IRSensor

log = logging.getLogger(__name__)

class IRHistory(object):
    """ Use the API calls as defined in Phidgeter objects, change the
    calling nomenclature to match bluegraph simulation classes.
    """
    def __init__(self, size=1000):
        log.debug("IR History Phidgeter wrapper")
        self.connected = False
        self.size = size
        self.history = deque()

    def connect(self):
        """ Establish connection to actual phidget hardware.
        """
        self.sensor = IRSensor()
        self.sensor.open_phidget()
        self.connected = True
        return self.connected

    def read(self):
        """ Get actual data from the phidget device.
        """
        result = self.sensor.get_temperature()
        self.history.append(result)

        if len(self.history) > self.size:
            self.history.popleft()

        #print("History is %s", self.history)
        return self.history

    def disconnect(self):
        """ Close the connection to the phidget hardware.
        """
        print "In disconnect call"
        self.sensor.close_phidget()
        self.connected = False
        return True
