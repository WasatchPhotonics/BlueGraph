""" GUI components for the BlueGraph application.
"""

from PySide import QtGui

class Basic(QtGui.QMainWindow):
    """ The most basic window possible for testing pyside, xvfb and
    travis integration.
    """
    def __init__(self):
        super(Basic, self).__init__()
        self.lblInfo = QtGui.QLabel("Default")

        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.lblInfo)
        self.setLayout(self.hbox)

        self.setGeometry(0, 0, 800, 600)
        self.show()

