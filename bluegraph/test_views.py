""" unit and functional tests for bluegraph application.
"""

import os
import sys
import time
import numpy
import logging
import unittest

from PySide import QtGui, QtTest, QtCore

from bluegraph import views

# All the classes below will reuese this qapplication
app = QtGui.QApplication([])

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class TestBasicGraphInterface(unittest.TestCase):
    def setUp(self):
        self.form = views.Basic()

    def tearDown(self):
        log.info("Is the close all necessary?")
        app.closeAllWindows()

    def test_label_is_available_on_fedora_and_xvfb(self):
        self.assertEqual(self.form.lblInfo.text(), "Default")
        
        QtTest.QTest.qWaitForWindowShown(self.form) 

        self.assertEqual(self.form.width(), 800)
        self.assertEqual(self.form.height(), 600)

class TestPixmapBackedGraph(unittest.TestCase):
    def setUp(self):
        self.form = views.PixmapBackedGraph()

    def test_graph_starts_with_default_text(self):
        display = self.form.graphback.title
        self.assertEqual(display.text(), "BLUE GRAPH")

    def test_graph_starts_with_default_icon(self):
        icon = self.form.graphback.icon.boundingRect()
        
        self.assertEqual(icon.width(), 23)
        self.assertEqual(icon.height(), 23)

if __name__ == "__main__":
    unittest.main()
