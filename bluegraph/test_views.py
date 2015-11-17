""" unit and functional tests for bluegraph application.
"""

import os
import sys
import time
import logging
import unittest

from PySide import QtGui, QtTest, QtCore

from bluegraph.views import Basic

# All the classes below will reuese this qapplication
app = QtGui.QApplication([])

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class TestBasicGraphInterface(unittest.TestCase):
    def setUp(self):
        self.form = Basic()

    def tearDown(self):
        log.info("Is the close all necessary?")
        app.closeAllWindows()

    def test_label_is_available_on_fedora_and_xvfb(self):
        self.assertEqual(self.form.lblInfo.text(), "Default")
        
        QtTest.QTest.qWaitForWindowShown(self.form) 

        self.assertEqual(self.form.width(), 800)
        self.assertEqual(self.form.height(), 600)

    def test_svg_border_startup_size(self):
        self.assertEqual(self.form.lblInfo.text(), "Default")
        
        QtTest.QTest.qWaitForWindowShown(self.form) 

        self.assertEqual(self.form.width(), 800)
        self.assertEqual(self.form.height(), 600)
               

if __name__ == "__main__":
    unittest.main()
