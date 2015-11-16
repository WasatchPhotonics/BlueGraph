""" BlueGraph application controller
"""

import csv
import numpy
import logging

from PyQt4 import QtGui, QtCore

log = logging.getLogger(__name__)

class BlueGraph(QtGui.QMainWindow):
    """ The main interface for the BlueGraph application. Can be created
    from unittest or a main() for full test coverage.
    """
    def __init__(self):
        super(BlueGraph, self).__init__()
        #log.debug("creation")

        self.setGeometry(450, 350, 1080, 600)
        self.show()
