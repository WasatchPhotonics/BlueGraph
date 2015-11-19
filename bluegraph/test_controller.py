""" unit and functional tests for bluegraph application.
"""

import os
import sys
import time
import numpy
import logging
import unittest

from PySide import QtGui, QtTest, QtCore

from bluegraph import views, control

from bluegraph.devices import Simulation

log = logging.getLogger()
log.setLevel(logging.DEBUG)
strm = logging.StreamHandler(sys.stderr)
frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
strm.setFormatter(frmt)
log.addHandler(strm)


# Catch qapplication re-use runtime errors from nosetests if a
# previously loaded module has started a qapplication. Note that there
# is a now a unspecified app variable providing qt services if this is
# the case.
try:
    # All the classes below will reuese this qapplication
    app = QtGui.QApplication([])
except RuntimeError:
    log.critical("Runtime")


class TestController(unittest.TestCase):
    def setUp(self):
        self.control = control.BlueGraphController()

    def test_control_creates_simulation_device(self):
        self.assertIsInstance(self.control.device,
                              Simulation.SimulatedLaserPowerMeter)

    def test_control_creates_bluegraph_widget(self):
        form = self.control.form
        self.assertEqual(form.width(), 805)
        self.assertEqual(form.height(), 355)

    def test_control_fps_is_available(self):
        fps = self.control.fps
        time.sleep(3)
        self.assertLess(fps.rate(), 1000)
        self.assertGreater(fps.rate(), 1)
        app.exec_()
        app.closeAllWindows()

if __name__ == "__main__":
    unittest.main()
