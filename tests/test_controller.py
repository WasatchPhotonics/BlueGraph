""" unit and functional tests for bluegraph application.
"""
import sys
import logging

from PySide import QtTest

from bluegraph import control
from bluegraph.devices import Simulation


log = logging.getLogger()
strm = logging.StreamHandler(sys.stderr)
frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
strm.setFormatter(frmt)
log.addHandler(strm)
log.setLevel(logging.INFO)

class TestControllerMinMax:
    def test_control_links_min_and_max_to_data(self, qtbot):
        simulator = control.BlueGraphController()

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        min_text = simulator.form.graphback.minimum.text
        max_text = simulator.form.graphback.maximum.text
        assert min_text == "100.00"
        assert max_text == "65535.00"

class TestControllerSpeed:
    def test_control_creates_bluegraph_widget(self, qtbot):
        simulator = control.BlueGraphController()
        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()
        assert simulator.form.width() > 5
        assert simulator.form.height() > 5
        # These work on local fedora, fail on travis CI
        #assert simulator.form.width() == 805
        #assert simulator.form.height() == 355

    def test_close_event_triggered(self, qtbot):
        simulator = control.BlueGraphController()
        QtTest.QTest.qWaitForWindowShown(simulator.form)

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        simulator.form.closeEvent(None)

    def test_data_fps_and_render_fps_avialable(self, qtbot):
        simulator = control.BlueGraphController()

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        assert simulator.render_fps.rate() > 2
        assert simulator.data_fps.rate() > 2

    def test_data_and_render_regulated_to_same_speed_dev(self, qtbot):
        simulator = control.BlueGraphController()

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        assert simulator.render_fps.rate() == simulator.data_fps.rate()

    def test_nonblocking_regulated_render_fps_is_faster(self, qtbot):
        dev_class = "DeviceWrappers"
        dev_type = "NonBlockingInterface"
        dev_args = "RegulatedSpectra"
        cb = control.BlueGraphController
        simulator = cb(device_class=dev_class,
                       device_type=dev_type,
                       device_args=dev_args)

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        render_rate = simulator.render_fps.rate()
        data_rate = simulator.data_fps.rate()
        log.info("Rates: %s, %s", render_rate, data_rate)
        assert simulator.render_fps.rate() > simulator.data_fps.rate()
        simulator.form.closeEvent(None)

    def test_nonblocking_unregulated_render_fps_is_faster(self, qtbot):
        dev_class = "DeviceWrappers"
        dev_type = "NonBlockingInterface"
        dev_args = "SimulatedSpectra"
        cb = control.BlueGraphController
        simulator = cb(device_class=dev_class,
                       device_type=dev_type,
                       device_args=dev_args)


        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        render_rate = simulator.render_fps.rate()
        data_rate = simulator.data_fps.rate()
        log.info("Rates: %s, %s", render_rate, data_rate)
        assert simulator.render_fps.rate() > simulator.data_fps.rate()
        simulator.form.closeEvent(None)

class TestControllerDevices:
    def test_control_creates_simulation_device(self, qtbot):
        simulator = control.BlueGraphController()
        assert isinstance(simulator.device, Simulation.SimulatedDevice)

    def test_default_device_strip_chart_mode(self, qtbot):
        dev_class = "Simulation"
        dev_type = "StripChartDevice"
        dev_args = None
        cb = control.BlueGraphController
        simulator = cb(device_class=dev_class,
                       device_type=dev_type,
                       device_args=dev_args)

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        # Total number of data points in plots is greater than a minimum
        points = simulator.form.curve.getData()
        assert len(points[0]) < 20

        # Wait a longer time, make sure the graph continues to update
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()
        points = simulator.form.curve.getData()
        assert len(points[0]) == 20

        # Make sure graph rolls at maximum
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()
        points = simulator.form.curve.getData()
        assert len(points[0]) == 20

