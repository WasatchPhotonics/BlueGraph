""" Application control logic for the BlueGraph tool
"""

import sys
import numpy
import logging

from PySide import QtCore, QtGui

from bluegraph import views
from bluegraph.devices import Simulation

from bluegraph import utils

log = logging.getLogger(__name__)

class BlueGraphController(object):
    def __init__(self, data_source="SimulatedLaser"):

        if data_source == "SimulatedSpectra":
            self.device = Simulation.SimulatedSpectra()
        else:
            self.device = Simulation.SimulatedLaserPowerMeter()

        self.form = views.PixmapBackedGraph()

        log.debug("pixmap graph setup")

        self.fps = utils.SimpleFPS()

        self.setup_fps_timer()

        self.connect_signals()

    def connect_signals(self):
        """ Hook into GUI control signals from main controller.
        """
        self.form.exit_signal.exit.connect(self.close)

        class ControlClose(QtCore.QObject):
            exit = QtCore.Signal(str)

        self.control_exit_signal = ControlClose()


    def close(self, event):
        """ Cleanup and exit. Don't issue qapplication quit here,
        as that will terminate the qapplication during tests. Use the
        qapplication control from py.test.
        """
        log.debug("blue graph controller level close")
        self.data_timer.stop()
        self.control_exit_signal.exit.emit("control exit")

    def setup_fps_timer(self):
        """ Update the display Frames per second at every qt event
        timeout.
        """
        self.data_timer = QtCore.QTimer()
        self.data_timer.setSingleShot(True)
        self.data_timer.timeout.connect(self.update_fps)
        self.data_timer.start(0)

    def update_fps(self):
        """ Add tick, display the current rate.
        """
        rnd_data = numpy.random.uniform(1, 65535, 2048)
        self.form.curve.setData(rnd_data)

        self.fps.tick()
        fps_text = "Update: %s FPS" % self.fps.rate()
        #log.debug(fps_text)
        self.form.graphback.fps.setText(self.fps.rate())
        self.data_timer.start(0)
