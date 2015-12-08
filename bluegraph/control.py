""" Application control logic for the BlueGraph tool
"""

import sys
import numpy
import logging

from PySide import QtCore

from bluegraph import views
from bluegraph import utils

## __all__ in __init__ refines this list:
#from bluegraph.devices import *

log = logging.getLogger(__name__)


class BlueGraphController(object):
    def __init__(self, device_class="Simulation",
                 device_type="RegulatedSpectra",
                 device_args=None):

        title = device_type.upper()
        print "Class: %s, type: %s" % (device_class, device_type)


        try:
            cmd_name = "bluegraph.devices.%s" % device_class
            from_list = "bluegraph.devices"
            command_module = __import__(cmd_name, fromlist=from_list)
        except ImportError as exc:
            print "Exception importing %s" % exc

        self.device = eval("command_module.%s()" % device_type)
        #device_str = "%s.%s" % (device_class, device_type)
        #eval_device = eval(device_str)

        #if device_args != None:
            #self.device = eval_device(device_args)
        #else:
            #self.device = eval_device()

        self.device.connect()

        self.form = views.PixmapBackedGraph(title=title)

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
            self.update_min_max(rnd_data)

        self.render_fps.tick()
        new_fps = "D: %s\nR: %s" % (self.data_fps.rate(), self.render_fps.rate())
        self.form.graphback.view_fps.setText(new_fps)
        self.data_timer.start(0)

    def update_min_max(self, rnd_data):
        """ Show the current min and maximum values in the interface
        controls.
        """
        min_conv = numpy.min(rnd_data)
        self.form.graphback.minimum.setText(min_conv)

        max_conv = numpy.max(rnd_data)
        self.form.graphback.maximum.setText(max_conv)
