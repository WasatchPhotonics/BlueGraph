""" unit and functional tests for bluegraph application.
"""
import sys
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
    def test_layout_has_all_widgets(self, qtbot):

        simulator = multi_control.SensorsController()
        QtTest.QTest.qWaitForWindowShown(simulator.form)

        signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(signal, timeout=2000):
            simulator.form.show()

        print "Position: %s" % simulator.amps_graph.y()
        assert simulator.amps_graph.pos().x() == 0
        assert simulator.amps_graph.pos().y() == 0

        assert simulator.ir_temp.pos().x() == 0
        assert simulator.ir_temp.pos().y() == 362

        assert simulator.humidity.pos().x() == 0
        assert simulator.humidity.pos().y() == 724

        #simulator.form.closeEvent(None)
