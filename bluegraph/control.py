""" Application control logic for the BlueGraph tool
"""

import sys
import numpy
import logging

from PySide import QtCore

from bluegraph import views
from bluegraph.devices import Simulation

from linegrab import utils

log = logging.getLogger(__name__)

class BlueGraphController(object):
    def __init__(self):
        self.device = Simulation.SimulatedLaserPowerMeter()
        
        self.form = views.PixmapBackedGraph()

        log.debug("pixmap graph setup")

        self.fps = utils.SimpleFPS()

        self.setup_fps_timer()

    def setup_fps_timer(self):
        """ Update the display Frames per second at every qt event
        timeout.
        """
        #for item in range(10):
            #self.fps.tick()
        #log.debug("setup fps timer %s", self.fps.rate())
        self.data_timer = QtCore.QTimer()
        self.data_timer.timeout.connect(self.update_fps)
        self.data_timer.start(0)

    def update_fps(self):
        """ Add tick, display the current rate.
        """
        self.fps.tick()
        fps_text = "Update: %s FPS" % self.fps.rate()
        #log.debug(fps_text)
        self.data_timer.start(0)

