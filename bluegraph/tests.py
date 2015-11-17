""" unit and functional tests for bluegraph application.
"""

import os
import sys
import time
import logging
import unittest

from PyQt4 import QtGui, QtTest, QtCore

from bluegraph.devices import Simulation
# All the classes below will reuese this qapplication
#app = QtGui.QApplication([])

log = logging.getLogger()
log.setLevel(logging.DEBUG)

strm = logging.StreamHandler(sys.stderr)
frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
strm.setFormatter(frmt)
log.addHandler(strm)

class TestSimulatedLaserPowerMeter(unittest.TestCase):
    def setUp(self):
        self.device = Simulation.SimulatedLaserPowerMeter()

    def tearDown(self):
        self.device.close()
        self.assertFalse(self.device.is_open())

    def test_list_hardware_returns_simulated_device(self):
        dev_list = self.device.list_hardware()
        dev_str = "Simulated PM100"
        self.assertEqual(dev_str, dev_list[0])
            
    def test_connect_simulated_device_returns_ok(self):
        self.assertTrue(self.device.connect()) 
        self.assertTrue(self.device.is_open())

    def test_get_stream_returns_10_reads_per_second(self):        
        self.device.connect()
        start_time = time.time()
        for i in range(10):
            self.device.read()
        end_time = time.time()
      
        time_diff = end_time - start_time 
        self.assertTrue(time_diff < 1.1)
        self.assertTrue(time_diff > 0.9)

    def test_stream_data_is_randomized(self):
        self.device.connect()
        first = self.device.read()
        self.assertTrue(first != self.device.read())
 
if __name__ == "__main__":
    unittest.main()
