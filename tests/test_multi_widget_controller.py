""" unit and functional tests for bluegraph application.
"""
import sys
import pytest
import logging

from PySide import QtTest

from bluegraph import multi_control

log = logging.getLogger()
strm = logging.StreamHandler(sys.stderr)
frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
strm.setFormatter(frmt)
log.addHandler(strm)
log.setLevel(logging.INFO)

class TestSensorWidgetLayout:

    @pytest.mark.xfail
    def test_multi_sensors_available(self, qtbot):
        simulator = multi_control.SensorsController()
        QtTest.QTest.qWaitForWindowShown(simulator.form)

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        expected_y = 0
        for graph in simulator.sensor_list:
            print "Position: %s" % graph.y()
            assert graph.pos().x() == 0
            assert graph.pos().y() == expected_y
            expected_y += 362

        simulator.form.closeEvent(None)

    @pytest.mark.xfail
    def test_multi_sensors_updating(self, qtbot):
        simulator = multi_control.SensorsController()
        QtTest.QTest.qWaitForWindowShown(simulator.form)

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        cue_reads = []
        for sensor in simulator.sensor_list:
            cue_reads.append(sensor.curve.getData()[1])

        with qtbot.wait_signal(signal, timeout=4000):
            simulator.form.show()

        end_reads = []
        for sensor in simulator.sensor_list:
            end_reads.append(sensor.curve.getData()[1])


        assert cue_reads[0] != end_reads[0]
        assert cue_reads[1] != end_reads[1]
        assert cue_reads[2] != end_reads[2]

        simulator.form.closeEvent(None)

    @pytest.mark.xfail
    def test_multi_sensors_min_max_updating(self, qtbot):
        simulator = multi_control.SensorsController()

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        for sensor in simulator.sensor_list:
            min_text = sensor.graphback.minimum.text
            max_text = sensor.graphback.maximum.text
            assert min_text != "123.45"
            assert max_text != "987.65"

        simulator.form.closeEvent(None)

    @pytest.mark.xfail
    def test_multi_sensors_fps_is_updating(self, qtbot):
        simulator = multi_control.SensorsController()

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        for sensor in simulator.sensor_list:
            fps_text = sensor.graphback.view_fps.text
            assert fps_text != "9999"

        simulator.form.closeEvent(None)

