""" GUI components for the BlueGraph application.
"""

import logging

import numpy
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

class oreigBasicSVG(QtGui.QMainWindow):
    """ A basic SVG layout for pyside testing.
    """
    def __init__(self):
        super(BasicSVG, self).__init__()

        self.setWindowTitle("pyqtgraph in svg wrapper")
        #self.resize(1250, 550)

        # Establish the layout, central widget which may be necessary
        # for properly encapsulating the pyqtgraph widget/graphicsitem
        # so it can inherit offset position from the svg widget
        self.container_widget = QtGui.QWidget()
        self.setCentralWidget(self.container_widget)
        self.main_layout = QtGui.QVBoxLayout()
        self.container_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

       
        self.scene = QtGui.QGraphicsScene()

        filename = "bluegraph/assets/border_graph.svg"
        self.border = QtSvg.QGraphicsSvgItem(filename)
        result = self.scene.addItem(self.border)

        self.plot = pyqtgraph.PlotWidget(name="plotsub")
        self.result = self.scene.addWidget(self.plot)
        self.result.setParentItem(self.border) 
        self.result.setPos(100, 100)
        self.result.setGeometry(QtCore.QRectF(40, 50, 700, 250))

        self.view = QtGui.QGraphicsView(self.scene)
        self.main_layout.addWidget(self.view)

        
        nru = numpy.random.uniform
        low_data = nru(100, 200, 2048)
        self.curve = self.plot.plot(low_data)
        self.show()

        self.timer = QtCore.QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.update_graph)

    def update_graph(self):

        nru = numpy.random.uniform
        low_data = nru(100, 200, 2048)
        self.curve.setData(low_data)
        

class BasicSVG(QtGui.QMainWindow):
    """ A basic SVG layout for pyside testing.
    """
    def __init__(self):
        super(BasicSVG, self).__init__()

        self.scene = QtGui.QGraphicsScene()

        filename = "bluegraph/assets/border_graph.svg"
        self.border = QtSvg.QGraphicsSvgItem(filename)
        result = self.scene.addItem(self.border)

        self.plot = pyqtgraph.PlotWidget(name="plotsub")

        # This pattern is the key - You'd think you can just do
        # self.plot.setParentItem(self.border), then add it to
        # the scene (or don't). That will not place the widget as a
        # child of the border svg. You have to get the result of the
        # addwidget method and set the parent item on that
        self.result = self.scene.addWidget(self.plot)
        self.result.setParentItem(self.border) 
        self.result.setGeometry(QtCore.QRectF(40, 50, 700, 250))

        self.view = QtGui.QGraphicsView(self.scene)

        ramp_data = numpy.linspace(0, 2047, 2048)
        
        self.curve = self.plot.plot(ramp_data)
        self.scale_factor = 1.0
        self.view.show()

        self.timer = QtCore.QTimer()
        self.timer.start(1)
        self.timer.timeout.connect(self.update_timer_graph)

    def update_graph(self, new_data):
        """ wrapper function to update the pyqtgraph line data, as well
        as any associated updates to the interface.
        """
        self.curve.setData(new_data)

    def update_timer_graph(self):
        nru = numpy.random.uniform
        low_data = nru(100, 200, 2048)
        #self.scale_factor -= 0.001
        #self.border.setScale(self.scale_factor)
        self.update_graph(low_data)
