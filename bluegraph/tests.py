""" unit and functional tests for bluegraph application.
"""

import os
import sys
import logging
import unittest

from PyQt4 import QtGui, QtTest, QtCore

from bluegraph import BlueGraph

# All the classes below will reuese this qapplication
#app = QtGui.QApplication([])

#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

#strm = logging.StreamHandler(sys.stderr)
#frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
#strm.setFormatter(frmt)
#log.addHandler(strm)

        
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
