""" bluegraph utils - classes and helper functions for the BlueGraph
application.
"""

from PySide import QtGui, QtCore

class Basic(QtGui.QMainWindow):
    """ The most basic window possible for testing pyside, xvfb and
    travis integration. Specifically requried for py.test to
    automatically generate the qapplication.
    """
    def __init__(self):
        super(Basic, self).__init__()
        self.lblInfo = QtGui.QLabel("Default")

        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.lblInfo)
        self.setLayout(self.hbox)

        self.setGeometry(0, 0, 800, 600)
        self.show()

class SimpleFPS(object):
    """ Use qtimer and a tick function to return the number of ticks
    returned for a simple FPS computation.
    """
    def __init__(self):
        super(SimpleFPS, self).__init__()
        self.fps = -1
        self.ticks = 0

        self.fps_timer = QtCore.QTimer()
        self.fps_timer.timeout.connect(self.update_fps)
        self.fps_timer.start(0)

    def update_fps(self):
        """ FPS computations are for the last second only.
        """
        self.fps = self.ticks
        self.ticks = 0
        self.fps_timer.start(1000)

    def rate(self):
        """ Return the most recently computed fps
        """
        return self.fps

    def tick(self):
        """ Add one to the total tick history
        """
        self.ticks += 1
