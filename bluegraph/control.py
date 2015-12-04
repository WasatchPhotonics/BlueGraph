""" Application control logic for the BlueGraph tool
"""

import sys
import numpy
import logging

from PySide import QtCore

from bluegraph import views
from bluegraph.devices import Simulation

from bluegraph import utils

log = logging.getLogger(__name__)

class BlueGraphController(object):
    def __init__(self, device_type="RegulatedSpectra"):
        self.device_type = device_type
        if device_type == "RegulatedSpectra":
            self.device = Simulation.RegulatedSpectra(2048)

        elif device_type == "SimulatedSpectra":
            self.device = Simulation.SimulatedSpectra(2048)

        elif device_type == "NonBlockingSimulatedSpectra":
            simnb = Simulation.NonBlockingInterface
            self.device = simnb("SimulatedSpectra")

        elif device_type == "NonBlockingRegulated":
            simnb = Simulation.NonBlockingInterface
            self.device = simnb("RegulatedSpectra")

        self.device.connect()

        self.form = views.PixmapBackedGraph()

        log.debug("pixmap graph setup")

        self.render_fps = utils.SimpleFPS()
        self.data_fps = utils.SimpleFPS()

        self.setup_fps_timers()

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
        self.device.disconnect()
        self.control_exit_signal.exit.emit("control exit")


    def setup_fps_timers(self):
        """ Update the display Frames per second at every qt event
        timeout.
        """
        #for item in range(10):
            #self.fps.tick()
        #log.debug("setup fps timer %s", self.fps.rate())
        self.data_timer = QtCore.QTimer()
        self.data_timer.timeout.connect(self.update_fps)
        self.data_timer.setSingleShot(True)
        self.data_timer.start(0)

    def update_fps(self):
        """ Add tick, display the current rate.
        """
        rnd_data = self.device.read()
        if rnd_data is not None:
            self.form.curve.setData(rnd_data)
            self.data_fps.tick()
            self.form.graphback.data_fps.setText(self.data_fps.rate())

        self.render_fps.tick()
        self.form.graphback.render_fps.setText(self.render_fps.rate())
        self.data_timer.start(0)
