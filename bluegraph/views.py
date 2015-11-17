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


class BasicSVG(QtGui.QMainWindow):
    """ A basic SVG layout for pyside testing.
    """
    def __init__(self):
        super(BasicSVG, self).__init__()

        self.setWindowTitle("pyqtgraph in svg wrapper")
        self.resize(1250, 550)
        self.container_widget = QtGui.QWidget()
        self.setCentralWidget(self.container_widget)
        self.main_layout = QtGui.QVBoxLayout()
        self.container_widget.setLayout(self.main_layout)


        #mw = QtGui.QMainWindow()
        #mw.setWindowTitle('pyqtgraph example: PlotWidget')
        #mw.resize(1200,1200)
        #cw = QtGui.QWidget()
        #mw.setCentralWidget(cw)
        #l = QtGui.QVBoxLayout()
        #cw.setLayout(l)

        
        #scene = QtGui.QGraphicsScene()
        #graphics_text = QtGui.QGraphicsTextItem("graphcs text area test")
        #scene.addItem(graphics_text)

        #sub_plot = pg.PlotWidget(name="plotsub")
        #scene.addWidget(sub_plot)
        #
        #view = QtGui.QGraphicsView(scene)
        #l.addWidget(view)
        #
        #mw.show()
       
        self.scene = QtGui.QGraphicsScene()

        self.title = QtGui.QGraphicsTextItem("graphic title area")
        self.scene.addItem(self.title)

        filename = "bluegraph/assets/green_box.svg"
        filename = "bluegraph/assets/tall_graph_area.svg"
        filename = "bluegraph/assets/border_graph.svg"
        self.svg_back = QtSvg.QGraphicsSvgItem(filename)
        result = self.scene.addItem(self.svg_back)
        self.svg_back.setParentItem(self.title)

        self.plot_widget = pyqtgraph.PlotWidget(name="plotsub")
        #self.sub_plot.setContentsMargins(100, 100, 100, 100)
        self.result = self.scene.addWidget(self.plot_widget)
        self.result.setParentItem(self.svg_back) 
        self.result.setPos(100, 100)
        self.result.setGeometry(QtCore.QRectF(40, 50, 700, 250))

        self.view = QtGui.QGraphicsView(self.scene)
        self.main_layout.addWidget(self.view)

        
        
        #self.title.setPos(100, 100)

        nru = numpy.random.uniform
        low_data = nru(100, 200, 2048)
        self.curve = self.plot_widget.plot(low_data)
        self.show()

        self.timer = QtCore.QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.update_graph)

    def update_graph(self):

        nru = numpy.random.uniform
        low_data = nru(100, 200, 2048)
        self.curve.setData(low_data)
        
         
        #self.scene = QtGui.QGraphicsScene()
#
        #filename = "bluegraph/assets/green_box.svg"
        #self.svg_back = QtSvg.QGraphicsSvgItem(filename)
#
        #self.scene.addItem(self.svg_back)
#
        #self.new_graph = InternalGraph()
        #self.new_graph.setPos(100, 100)  
        #self.scene.addItem(self.new_graph)
#
        #self.direct_graph = pyqtgraph.PlotWidget()
        ##self.direct_graph.setParentItem(self.new_graph)
        #self.scene.addWidget(self.direct_graph)
        #self.direct_graph.setPos(200, 200)
         #
#
        #self.view = QtGui.QGraphicsView(self.scene)
        #self.view.show()


class InternalGraph(QtSvg.QGraphicsSvgItem):
    def __init__(self):
        super(InternalGraph, self).__init__()

        filename = "bluegraph/assets/small_red_box.svg"
        self.internal_box = QtSvg.QGraphicsSvgItem(filename, self)

        my_text = "testing internal" 
        self.text_desc = QtGui.QGraphicsSimpleTextItem(my_text)
        self.text_desc.setParentItem(self.internal_box)
        self.text_desc.setBrush(QtGui.QColor(255, 255, 255, 255) )
        self.text_desc.setPos(70, 15)
 
        ## Graph area
        #self.graph = self.make_graph()
        #self.graph.setParentItem(self.internal_box)
        
        #res = scene.addWidget(self.graph)
        #res.setParentItem(self)
        #res.setGeometry(QRectF(272, 25, 736,225))

        #self.render_initial_graph(graph_color)

    def make_graph(self):
        self.my_graph = pyqtgraph.PlotWidget()
        return self.my_graph

    def render_initial_graph(self, line_color):
        nru = numpy.random.uniform
        low_data = nru(100, 200, 2048)
        
        #self.graph = pyqtgraph.PlotWidget()
        self.graph = pyqtgraph.GraphicsLayoutWidget()
        #self.graph.setParentItem(self.svg_back)
        
        pass

    def make_transparent_graph(self, graph_color="green"):
        import guiqwt
        from guiqwt.styles import CurveParam
        import guiqwt.plot

        back = "background-color: rgba(0,0,0,255);\n" 

        self.white_on_clear = back + "color: rgba(255,255,255,255);"
        self.green_on_black = back + "color: rgba(0,212,85,255);"
        self.yellow_on_black = back + "color: rgba(255,212,42,255);"
        self.red_on_black = back + "color: rgba(255,0,0,255);"

        style = self.green_on_black
        if graph_color == "yellow":
            style = self.yellow_on_black
        elif graph_color == "red":
            style = self.red_on_black
        
        # Reduce the number of grid lines, make sure chart has light gray labels
        mygrid = guiqwt.styles.GridParam() 
        myls = guiqwt.styles.LineStyleParam()
        myls.color = "#333333"
        mygrid.maj_line = myls
        mygrid.min_line = myls
        main_chart_px = guiqwt.plot.CurveWidget(gridparam=mygrid)
        main_chart_px.setStyleSheet(style)
        return main_chart_px

       
    def mousePressEvent(self, event):
        print "mouse press"
        #self.setOpacity( self.opacity() - 0.1)
