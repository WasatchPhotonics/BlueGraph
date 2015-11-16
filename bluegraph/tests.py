""" unit and functional tests for bluegraph application.
"""

import os
import sys
import logging
import unittest

from PyQt4 import QtGui, QtTest, QtCore

from bluegraph import BlueGraph
from bluegraph.devices import Simulation
# All the classes below will reuese this qapplication
#app = QtGui.QApplication([])

#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

#strm = logging.StreamHandler(sys.stderr)
#frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
#strm.setFormatter(frmt)
#log.addHandler(strm)

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
            

    #def test_connect_simulated_device_returns_ok(self):

    #def test_get_stream_returns_10_reads_per_second(self):        
class TestBlueGraphScript(unittest.TestCase):

#    def tearDown(self):
        # This cleans up old windows from rapid tests
#        app.closeAllWindows()

#    def test_parser(self):
#        # Accept one option: testing, which causes the form to close
#        # itself which should only be used with the unittest as the
#        # controller. 
#        fgapp = BlueGraph.BlueGraphApplication()
#
        ## Fail with more than just -t
#        with self.assertRaises(SystemExit):
#            fgapp.parse_args(["-t", "-s"])
#            
#        args = fgapp.parse_args(["-t"])
#        self.assertTrue(args.testing)  

    def test_main_options(self):
        # Verify that main run with the testing option auto-closes the
        # application
        result = BlueGraph.main(["unittest", "-t"])
        self.assertEquals(0, result)
        
if __name__ == "__main__":
    unittest.main()
