""" multiple control element logic. Used for displaying multiple
bluegraph widgets in a single application.
"""

import sys
import numpy
import logging

from PySide import QtCore, QtGui

from bluegraph import views
from bluegraph import utils
from bluegraph.devices import DeviceWrappers

log = logging.getLogger(__name__)

class SensorsController(object):
    def __init__(self, device_class="Simulation",
                 device_type="RegulatedSpectra",
                 device_args=None,
                 title=None):

        if title == None:
            title = device_type.upper()


        self.form = views.MultiGraphLayout()


        self.amps_graph = views.PixmapBackedGraph("AMPS")
        self.form.vbox.addWidget(self.amps_graph)

        self.ir_temp = views.PixmapBackedGraph("IR TEMP")
        self.form.vbox.addWidget(self.ir_temp)

        self.humidity = views.PixmapBackedGraph("HUMIDITY")
        self.form.vbox.addWidget(self.humidity)

        self.sensor_list = []
        self.sensor_list.append(self.amps_graph)
        self.sensor_list.append(self.ir_temp)
        self.sensor_list.append(self.humidity)

        self.render_fps = utils.SimpleFPS()
        self.data_fps = utils.SimpleFPS()

        dev_wrap = DeviceWrappers.DeviceChooser()
        device_class = "DeviceWrappers"
        device_type = "NonBlockingInterface"
        device_args = "Simulation.StripChartDevice"

        for sensor in self.sensor_list:
            sensor.device = dev_wrap.create(device_class, device_type,
                                            device_args)
            sensor.device.connect()


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
        print("blue graph controller level close")
        for sensor in self.sensor_list:
            sensor.device.disconnect()
        self.control_exit_signal.exit.emit("control exit")


    def setup_fps_timers(self):
        """ Update the display Frames per second at every qt event
        timeout.
        """
        self.data_timer = QtCore.QTimer()
        self.data_timer.timeout.connect(self.update_fps)
        self.data_timer.setSingleShot(True)
        self.data_timer.start(0)

    def update_fps(self):
        """ Add tick, display the current rate.
        """
        for sensor in self.sensor_list:
            rnd_data = sensor.device.read()
            self.data_fps.tick()
            if rnd_data is not None:
                sensor.curve.setData(rnd_data)
                self.data_fps.tick()
                self.update_min_max(sensor, rnd_data)
                self.show_fps(sensor)

        self.render_fps.tick()
        self.data_timer.start(0)

    def show_fps(self, sensor):
        """ Primitive fps calculations of data and render fps.
        """
        new_fps = "D: %s\nR: %s" % (self.data_fps.rate(),
                                    self.render_fps.rate())
        sensor.graphback.view_fps.setText(new_fps)


    def update_min_max(self, sensor, rnd_data):
        """ Show the current min and maximum values in the interface
        controls.
        """
        min_conv = numpy.min(rnd_data)
        sensor.graphback.minimum.setText(min_conv)

        max_conv = numpy.max(rnd_data)
        sensor.graphback.maximum.setText(max_conv)
