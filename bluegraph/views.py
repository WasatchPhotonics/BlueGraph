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

class LayeredGraphDisplay(QtGui.QMainWindow):
    """ A main window with no border, stacked graphics view items with
    graphics effects, and other tests to match the existing raster
    graphics approach from ExtendedTest.
    """
    def __init__(self, title="BlueGraph"):
        super(LayeredGraphDisplay, self).__init__()

        # Bounding rect, draw with no visuals once laid out
        #   svg border with bounding rect as parent
        #   title with bounding rect as parent
        #   pyqtgraph with bounding rect as parent
        #   
        # This approach is so you can apply graphicseffects to the
        # bottom svg border without blurring out the graph itself.
        # Designed primarily for the soft border edges on the box. This
        # also lets you resize the items and keep the vector graphics
        # qualities.
        #
        # An alternative here is to install QtWebKit, and take advantage
        # of a more complete SVG standards support, including blur
        # effects. SVG Items only support SVG Tiny, which you can work
        # around by blurring various components of the interface
        # directly.
        #
        # Another alternative used in the past is to make renderings
        # exported as pngs from inkscape. This gives a more 1to1
        # visualization and greater speed.  If you just blur the edge
        # svg graphic is that the appropriate compromise between
        # flexibility and design ease?
        #
        # Or, go right to pixmap
        # A Rect item - bare bones for portability, all of them are rect
        #  items
        #   has child pixmap item 
        #   pixmap item has child text item with font
        #   pixmap has child pyqtgraph item

        self.scene = QtGui.QGraphicsScene()

        self.border = RectBasedLayout(self.scene)
        result = self.scene.addItem(self.border)

        #self.small_box = MySvg("small_red_box")
        #result = self.scene.addItem(self.small_box)

        #self.plot = pyqtgraph.PlotWidget(name="plotsub")

        # This pattern is the key - You'd think you can just do
        # self.plot.setParentItem(self.border), then add it to
        # the scene (or don't). That will not place the widget as a
        # child of the border svg. You have to get the result of the
        # addwidget method and set the parent item on that
        #self.result = self.scene.addWidget(self.plot)
        #self.result.setParentItem(self.border) 
        #self.result.setGeometry(QtCore.QRectF(40, 50, 700, 250))

        self.view = QtGui.QGraphicsView(self.scene)

        self.view.show()
        window_size = QtCore.QRect(100, 100, 800, 600)
        self.setGeometry(window_size)
        self.show()

        ramp_data = numpy.linspace(0, 2047, 2048)
        #self.curve = self.plot.plot(ramp_data)
        self.scale_factor = 1.0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer_graph)
        #self.timer.start(1)
        self.mouseMoveEvent(None)

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
    def mousePressEvent(self, event):
        log.info("Clicked")
        self.event_sig.clicked.emit( self._on_filename )

    def mouseMoveEvent(self, event):
        print "mouse move event"
        log.warning("Hover")


class RectBasedLayout(QtGui.QGraphicsRectItem):
    def __init__(self, scene, title="BlueGraph"):
        super(RectBasedLayout, self).__init__()

        large_rect = QtCore.QRectF(100, 50, 700, 250)
        self.setPen(QtGui.QPen(QtGui.QColor(255,0,0,255)))
        self.setRect(large_rect)

        #filename = "bluegraph/assets/border_graph.svg"
        #self.svg_border = QtSvg.QGraphicsSvgItem(filename)
        #result = scene.addItem(self.svg_border)
        #self.svg_border.setParentItem(self)

        #self.plot = pyqtgraph.PlotWidget(name="plotsub")
        #result = scene.addWidget(self.plot)
        #result.setParentItem(self.svg_border)
        #result.setParentItem(self)

        #small_rect = QtCore.QRectF(50, 25, 350, 125)
        #result.setGeometry(small_rect)
        self.mousePressEvent(None)

        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setAcceptsHoverEvents(True)

    def mousePressEvent(self, event):
        log.info("Clicked")

    def hoverMoveEvent(self, event):
        log.debug("Hover")
      

    def mouseMoveEvent(self, event):
        print "mouse move event"
        log.warning("Hover")

class MySvg(QtSvg.QGraphicsSvgItem):
    def __init__(self, filen='empty_box.svg' ):
        self.prefix = "bluegraph/assets"
        self._filename = "%s/%s.svg" % (self.prefix, filen)
        parent = super( MySvg, self ).__init__(self._filename)

        self.setFlags( QtGui.QGraphicsItem.ItemIsSelectable )

        self.setAcceptsHoverEvents(True)
        self._status = "default"
    
        self.hover_svg = None

    def hoverEnterEvent(self, event):
        #print 'Enter'
        if self.hover_svg is None: return
        self.renderer().load(  self.prefix + self.hover_svg )

    def hoverLeaveEvent(self, event):
        #print 'Leave'
        self.renderer().load(  self.prefix + self._filename )

    def hoverMoveEvent(self, event):
        #print 'Moving'
        pass
      
    def mousePressEvent(self, event):
        print "mouse press"
        #self.setOpacity( self.opacity() - 0.1)

    def show_invalid( self ):
        # Display the animated svg when the invalid condition is set
        self.renderer().load( self.prefix + 'animate_exam_process.svg' )

    def show_default( self ):
        self.renderer().load( self.prefix + self._filename )
    #def show_process(self):
        #if self._status != "process":
            #self.renderer().load( self.prefix + 'animate_exam_process.svg')
        #self._status = "process"
#
    #def show_default(self):
        #if self._status != "default":
            #self.renderer().load( self.prefix + 'animate_exam_default.svg')
        #self._status = "default"

class FormBasic(QtGui.QMainWindow):
    def __init__(self):
        super(FormBasicSVG, self).__init__()


        # Establish the layout, central widget which may be necessary
        # for properly encapsulating the pyqtgraph widget/graphicsitem
        # so it can inherit offset position from the svg widget
        self.setWindowTitle("form test")
        self.resize(1250, 550)
        self.container_widget = QtGui.QWidget()
        self.setCentralWidget(self.container_widget)
        self.main_layout = QtGui.QVBoxLayout()
        self.container_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)


       
        #self.scene = QtGui.QGraphicsScene()
#
        #filename = "bluegraph/assets/border_graph.svg"
        #self.border = QtSvg.QGraphicsSvgItem(filename)
        #result = self.scene.addItem(self.border)
#
        #self.plot = pyqtgraph.PlotWidget(name="plotsub")
        #self.result = self.scene.addWidget(self.plot)
        #self.result.setParentItem(self.border) 
        #self.result.setPos(100, 100)
        #self.result.setGeometry(QtCore.QRectF(40, 50, 700, 250))
#
        #self.view = QtGui.QGraphicsView(self.scene)
        #self.main_layout.addWidget(self.view)
#
        #
        #nru = numpy.random.uniform
        #low_data = nru(100, 200, 2048)
        #self.curve = self.plot.plot(low_data)

        # Establish the form first to place the graphics view in,
        # otherwise it will require view.show and not respect the parent
        # rectitem size. If you do self.show it will show a separate
        # window
        self.scene = QtGui.QGraphicsScene()

        large_rect = QtCore.QRectF(0, 0, 700, 250)
        red_pen = QtGui.QPen(QtGui.QColor(255,0,0,255))
        self.red_rect = QtGui.QGraphicsRectItem(large_rect)
        self.red_rect.setPen(red_pen)
        result = self.scene.addItem(self.red_rect)


        sub_blue_rect = QtCore.QRectF(0, 0, 600, 200)
        blue_pen = QtGui.QPen(QtGui.QColor(0, 0, 255, 255))
        self.blue_rect = QtGui.QGraphicsRectItem(sub_blue_rect)
        self.blue_rect.setPen(blue_pen)
        result = self.scene.addItem(self.blue_rect)
        self.blue_rect.setPos(150, 0)

        inside_rect = QtCore.QRectF(0, 0, 350, 125)
        green_pen = QtGui.QPen(QtGui.QColor(0,255,0,255))
        self.green_rect = QtGui.QGraphicsRectItem(inside_rect,
                                                  parent=self.blue_rect)
        self.green_rect.setPen(green_pen)
        #result = self.scene.addItem(self.green_rect)
        #result.setParentItem(self.red_rect)
        #self.green_rect.setParentItem(self.red_rect)
        self.green_rect.setPos(100, 150)
    
        # Clip green rect at blue rect border
        self.blue_rect.setFlag(QtGui.QGraphicsItem.ItemClipsChildrenToShape)

        self.plot = pyqtgraph.PlotWidget(name="plotsub")
        self.result = self.scene.addWidget(self.plot)
        self.result.setParentItem(self.blue_rect) 
        #self.result.setGeometry(QtCore.QRectF(0, 0, 600, 150))
    
        blue_size = self.blue_rect.boundingRect()
        self.result.setGeometry(blue_size)
        self.result.setPos(100, 0)



        self.view = QtGui.QGraphicsView(self.scene)
        self.main_layout.addWidget(self.view)
        self.show()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer_graph)
        #self.timer.start(1)

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



class FormBasicSVG(QtGui.QMainWindow):
    def __init__(self):
        super(FormBasicSVG, self).__init__()


        # Establish the layout, central widget which may be necessary
        # for properly encapsulating the pyqtgraph widget/graphicsitem
        # so it can inherit offset position from the svg widget
        self.setWindowTitle("form test")
        self.resize(1250, 550)
        self.container_widget = QtGui.QWidget()
        self.setCentralWidget(self.container_widget)
        self.main_layout = QtGui.QVBoxLayout()
        self.container_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)


       
        #self.scene = QtGui.QGraphicsScene()
#
        #filename = "bluegraph/assets/border_graph.svg"
        #self.border = QtSvg.QGraphicsSvgItem(filename)
        #result = self.scene.addItem(self.border)
#
        #self.plot = pyqtgraph.PlotWidget(name="plotsub")
        #self.result = self.scene.addWidget(self.plot)
        #self.result.setParentItem(self.border) 
        #self.result.setPos(100, 100)
        #self.result.setGeometry(QtCore.QRectF(40, 50, 700, 250))
#
        #self.view = QtGui.QGraphicsView(self.scene)
        #self.main_layout.addWidget(self.view)
#
        #
        #nru = numpy.random.uniform
        #low_data = nru(100, 200, 2048)
        #self.curve = self.plot.plot(low_data)

        # Establish the form first to place the graphics view in,
        # otherwise it will require view.show and not respect the parent
        # rectitem size. If you do self.show it will show a separate
        # window
        self.scene = QtGui.QGraphicsScene()

        large_rect = QtCore.QRectF(0, 0, 700, 250)
        red_pen = QtGui.QPen(QtGui.QColor(255,0,0,255))
        self.red_rect = QtGui.QGraphicsRectItem(large_rect)
        self.red_rect.setPen(red_pen)
        result = self.scene.addItem(self.red_rect)

        # Clip green rect at blue rect border
        #self.red_rect.setFlag(QtGui.QGraphicsItem.ItemClipsChildrenToShape)

        self.plot = pyqtgraph.PlotWidget(name="plotsub")
        self.result = self.scene.addWidget(self.plot)
        self.result.setParentItem(self.red_rect) 
        #self.result.setGeometry(QtCore.QRectF(0, 0, 600, 150))
    
        red_size = self.red_rect.boundingRect()
        self.result.setGeometry(red_size)
        #self.result.setPos(100, 0)


        self.view = QtGui.QGraphicsView(self.scene)
        self.main_layout.addWidget(self.view)
        self.show()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer_graph)
        #self.timer.start(1)

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

    def mousePressEvent(self, event):
        print "mouse press"
        #self.setOpacity( self.opacity() - 0.1)


class ClassRects(QtGui.QMainWindow):
    def __init__(self):
        super(ClassRects, self).__init__()


        # Establish the layout, central widget which may be necessary
        # for properly encapsulating the pyqtgraph widget/graphicsitem
        # so it can inherit offset position from the svg widget
        self.setWindowTitle("form test")
        self.resize(1250, 550)
        self.container_widget = QtGui.QWidget()
        self.setCentralWidget(self.container_widget)
        self.main_layout = QtGui.QVBoxLayout()
        self.container_widget.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.scene = QtGui.QGraphicsScene()

        large_rect = QtCore.QRectF(0, 0, 900, 400)
        red_pen = QtGui.QPen(QtGui.QColor(255,0,0,255))
        self.red_rect = QtGui.QGraphicsRectItem(large_rect)
        self.red_rect.setPen(red_pen)
        result = self.scene.addItem(self.red_rect)

        smaller_rect = QtCore.QRectF(0, 0, 800, 350)
        blue_pen = QtGui.QPen(QtGui.QColor(0, 0, 255, 255))
        self.blueish = Recter(smaller_rect, blue_pen)
        self.scene.addItem(self.blueish)

        inside_rect = QtCore.QRectF(0, 0, 783, 333)
        yellow_pen = QtGui.QPen(QtGui.QColor(255, 125, 0, 255))
        self.yellow_rect = Recter(inside_rect, yellow_pen)
        self.scene.addItem(self.yellow_rect)
        self.yellow_rect.setParentItem(self.blueish)


        filename = "bluegraph/assets/graph_export.png"
        #self.svg_raster = QtGui.QGraphicsPixmapItem(filename)
        #self.scene.addItem(self.svg_raster)
        #self.svg_raster.setParentItem(self.blueish)

        # Background only
        #self.pix_back = PixBackground(filename)
        #self.scene.addItem(self.pix_back)
        #self.pix_back.setParentItem(self.blueish)

        # pixmap background with rect in the middle
        #self.outline_back = OutlineBackground(filename)
        #self.scene.addItem(self.outline_back)
        #self.outline_back.setParentItem(self.blueish)
    
        # pixmap background with pyqtgraph in the middle
        #self.graphback = GraphBackground(filename)
        #self.scene.addItem(self.graphback)
        #self.graphback.setParentItem(self.blueish)
    
        # scene included pixmap background with pyqtgraph in the middle
        self.graphback = SceneGraphBackground(self.scene, filename)
        self.scene.addItem(self.graphback)
        self.graphback.setParentItem(self.blueish)
    

        self.blueish.setPos(50, 50)

        # Clip view at rect border, red is just another element, blue is
        # the parent of subs
        #self.red_rect.setFlag(QtGui.QGraphicsItem.ItemClipsChildrenToShape)
        self.blueish.setFlag(QtGui.QGraphicsItem.ItemClipsChildrenToShape)

        self.view = QtGui.QGraphicsView(self.scene)
        self.main_layout.addWidget(self.view)
        self.show()

        self.scale = 1.0
        ramp_data = numpy.linspace(0, 2047, 2048)
        self.curve = self.graphback.plot.plot(ramp_data)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer_graph)
        self.timer.start(1)

    def mousePressEvent(self, event):
        log.info("Clicked %s", event)
        self.blueish.setScale(self.scale)

        self.scale -= 0.01


    def update_timer_graph(self):
        nru = numpy.random.uniform
        low_data = nru(100, 200, 2048)
        self.update_graph(low_data)

    def update_graph(self, new_data):
        """ wrapper function to update the pyqtgraph line data, as well
        as any associated updates to the interface.
        """
        self.curve.setData(new_data)
        

class SceneGraphBackground(QtGui.QGraphicsPixmapItem):
    """ Like GraphBackground below, but include the scene parameter so
    certain widgets will add correctly. pyqtgraph plotwidget for
    example, requires that you add it to the scene first, then set the
    parent on the return of the addwidget command.
    """
    def __init__(self, scene, filename):
        super(SceneGraphBackground, self).__init__(filename)

        self.plot = pyqtgraph.PlotWidget(name="mystery")
        result = scene.addWidget(self.plot)
        result.setParentItem(self)
        self.plot.setGeometry(QtCore.QRect(40, 50, 700, 250))

        #sub_rect = QtCore.QRectF(0, 0, 383, 133)
        #yellow_pen = QtGui.QPen(QtGui.QColor(255, 125, 0, 255))
        #self.yellow_rect = Recter(sub_rect, yellow_pen)
        #self.yellow_rect.setParentItem(self)
        #self.yellow_rect.setPos(50, 50)

        #result = scene.addItem(self.yellow_rect)
        #result.setParentItem(self)



class GraphBackground(QtGui.QGraphicsPixmapItem):
    def __init__(self, filename):
        super(GraphBackground, self).__init__(filename)

        #self.plot = pyqtgraph.PlotWidget(name="plotsub")
        #self.result = self.scene.addWidget(self.plot)
        #self.result.setParentItem(self.red_rect) 
        #self.result.setGeometry(QtCore.QRectF(0, 0, 600, 150))

        # This is the failure mode. This is why you were getting
        # confused. If you do the rect addition below, it will add it,
        # and have the correct position and inheritance. If you do the
        # same with the plot as shown here, it just shows the left side
        # axis
        self.plot = pyqtgraph.PlotWidget(name="mystery")
        self.plot.setParentItem(self)
        self.plot.setGeometry(QtCore.QRect(0, 0, 100, 50))

        #sub_rect = QtCore.QRectF(0, 0, 383, 133)
        #yellow_pen = QtGui.QPen(QtGui.QColor(255, 125, 0, 255))
        #self.yellow_rect = Recter(sub_rect, yellow_pen)
        #self.yellow_rect.setParentItem(self)
        #self.yellow_rect.setPos(50, 50)


class OutlineBackground(QtGui.QGraphicsPixmapItem):
    def __init__(self, filename):
        super(OutlineBackground, self).__init__(filename)

        sub_rect = QtCore.QRectF(0, 0, 383, 133)
        yellow_pen = QtGui.QPen(QtGui.QColor(255, 125, 0, 255))
        self.yellow_rect = Recter(sub_rect, yellow_pen)
        self.yellow_rect.setParentItem(self)
        self.yellow_rect.setPos(50, 50)
        #self.scene.addItem(self.yellow_rect)
        #self.yellow_rect.setParentItem(self.blueish)

class PixBackground(QtGui.QGraphicsPixmapItem):
    def __init__(self, filename):
        super(PixBackground, self).__init__(filename)
         
    

class Recter(QtGui.QGraphicsRectItem):
    def __init__(self, size_rect, pen):
        super(Recter, self).__init__(size_rect)
        self.setPen(pen) 
         
        
    def mousePressEvent(self, event):
        log.info("Clicked %s", self.pen())
