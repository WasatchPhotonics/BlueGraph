""" GUI components for the BlueGraph application.
"""

import sys
import numpy
import logging

import pyqtgraph

from PySide import QtGui, QtSvg, QtCore

log = logging.getLogger(__name__)

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

class PixmapBackedGraph(QtGui.QWidget):
    def __init__(self):
        super(PixmapBackedGraph, self).__init__()

        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.scene = QtGui.QGraphicsScene()

        filename = "bluegraph/assets/graph_export.png"
        self.graphback = SceneGraphBackground(self.scene, filename)
        self.scene.addItem(self.graphback)

        self.view = QtGui.QGraphicsView(self.scene)
        view_style = ("background: transparent;"
                      "border: 0px"
                     )
        self.view.setStyleSheet(view_style)
        self.main_layout.addWidget(self.view)

        # Requires a compositing window manager to be translucent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() 
            | QtCore.Qt.WindowStaysOnTopHint)

        self.show()

        self.scale = 1.0
        ramp_data = numpy.linspace(0, 2047, 2048)
        self.curve = self.graphback.plot.plot(ramp_data)

    def closeEvent(self, event):
        log.debug("Pixmap level close")
        sys.exit()

class SceneGraphBackground(QtGui.QGraphicsPixmapItem):
    """ Like GraphBackground, but include the scene parameter so
    certain widgets will add correctly. pyqtgraph plotwidget for
    example, requires that you add it to the scene first, then set the
    parent on the return of the addWidget command.
    """
    def __init__(self, scene, filename, title="BLUE GRAPH",
                 icon="default"):
        super(SceneGraphBackground, self).__init__(filename)

        # The plot widget
        self.plot = pyqtgraph.PlotWidget(name="mystery", pen=(0,0,255))
        result = scene.addWidget(self.plot)
        result.setParentItem(self)
        self.plot.setGeometry(QtCore.QRect(40, 50, 700, 250))

        # The main title
        font_name = "bluegraph/assets/fonts/GearsOfPeace.ttf"
        QtGui.QFontDatabase.addApplicationFont(font_name)

        # Filename will work on linux, actual font name with spaces is
        # required for success on windows
        self.default_font = QtGui.QFont("Gears of Peace")
        self.default_font.setPointSize( 10 )

        white = QtGui.QColor(255, 255, 255, 255)
        self.title = QtGui.QGraphicsSimpleTextItem(title)
        self.title.setPos(65, 20)
        self.title.setBrush(white)
        self.title.setParentItem(self)
        self.title.setFont(self.default_font)

        # The icon to the left of the main title
        icon_filename = "bluegraph/assets/default_icon.png"
        self.icon = QtGui.QGraphicsPixmapItem(icon_filename)
        self.icon.setPos(33, 13)
        self.icon.setParentItem(self)


