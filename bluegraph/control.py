""" Application control logic for the BlueGraph tool
"""

import sys
import zmq
import time
import numpy
import logging

from PySide import QtCore, QtGui

from bluegraph import views
from bluegraph import utils
from bluegraph.devices import Simulation
from bluegraph.devices import ZMQWrapper

log = logging.getLogger(__name__)

class BlueGraphController(object):
    def __init__(self, data_source="InternalSlow"):

        if data_source == "SimulatedSpectra":
            self.device = Simulation.SimulatedSpectra()

        elif data_source == "SimulatedLaser":
            self.device = Simulation.SimulatedLaserPowerMeter()

        elif data_source == "ZMQLaserPower":
            self.device = ZMQReader()
            self.zmq_pub = ZMQWrapper.Publisher("SimulatedLaserPower", 10)

        else:
            self.device = InternalSlow()

        self.device.connect()

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
        rnd_data = self.device.read()
        self.form.curve.setData(rnd_data)

        self.fps.tick()
        fps_text = "Update: %s FPS" % self.fps.rate()
        #log.debug(fps_text)
        self.form.graphback.fps.setText(self.fps.rate())
        self.data_timer.start(0)

class InternalSlow(object):
    """ force slow readback rate with data for testing.
    """
    def __init__(self):
        super(InternalSlow, self).__init__()

    def connect(self):
        return

    def read(self):
        """ return randomized data. Force to a slow speed for testing
        """
        start_time = time.time()
        rnd_data = numpy.random.uniform(1, 65535, 2048)

        time_diff = start_time - time.time()
        if time_diff < 0.100:
            time_wait = 0.100 - abs(time_diff)
            time.sleep(abs(time_wait))

        return rnd_data

class ZMQReader(object):
    """ Wrapper interface around the zmq socket to expose the same API
    as the direct simulation device.
    """
    def __init__(self):
        super(ZMQReader, self).__init__()
        log.debug("Setup zmq context and socket reader")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect ("tcp://127.0.0.1:5678")
        self.socket.setsockopt(zmq.SUBSCRIBE, "SimulatedLaserPower")

    def connect(self):
        """ setup zmq connection
        """
        log.debug("Connect placeholder")

    def read(self):

        result = self.socket.recv()
        log.debug("Got: %s", result)
        return result


        try:
            self.socket.RCVTIMEO = 1000
            result = self.socket.recv()
            log.debug("Got: %s", result)
            return result
            topic, value = result.split(",")
            return float(value)
        except Exception as exc:
            log.critical("Exception: %s", exc)

    def close(self):
        log.debug("close zmq reader")
