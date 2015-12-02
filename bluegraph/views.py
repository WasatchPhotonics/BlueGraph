""" GUI components for the BlueGraph application.
"""

import sys
import logging

import pyqtgraph

from PySide import QtGui, QtSvg, QtCore

from assets import bluegraph_resources_rc

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

        filename = ":ui/graph_export.png"
        self.graphback = SceneGraphBackground(self.scene, filename)
        self.scene.addItem(self.graphback)

        self.view = QtGui.QGraphicsView(self.scene)
        view_style = ("background: transparent;"
                      "border: 0px"
                     )
        self.view.setStyleSheet(view_style)
        self.setStyleSheet(view_style)
        self.main_layout.addWidget(self.view)

        # Requires a compositing window manager to be translucent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags()
            | QtCore.Qt.WindowStaysOnTopHint)

        self.show()

        self.scale = 1.0
        ramp_data = range(2048)
        self.curve = self.graphback.plot.plot(ramp_data)

        self.create_signals()

    def create_signals(self):
        """ Create signal objects to be used by controller.
        """
        class ViewClose(QtCore.QObject):
            exit = QtCore.Signal(str)

        self.exit_signal = ViewClose()

    def closeEvent(self, event):
        log.debug("Pixmap level close")
        self.exit_signal.exit.emit("close event")

class SceneGraphBackground(QtGui.QGraphicsPixmapItem):
    """ Like GraphBackground, but include the scene parameter so
    certain widgets will add correctly. pyqtgraph plotwidget for
    example, requires that you add it to the scene first, then set the
    parent on the return of the addWidget command.
    """
    def __init__(self, scene, filename, title="BLUE GRAPH",
                 icon="default"):
        super(SceneGraphBackground, self).__init__(filename)

        # The main font
        font_name = ":ui/fonts/GearsOfPeace.ttf"
        QtGui.QFontDatabase.addApplicationFont(font_name)


        # The plot widget. As a component of a qgraphicspixmapitem,
        # apparently the background=None does not actually set the
        # background to none. Override it with a background set to
        # transparent in the style sheet parameter
        self.plot = pyqtgraph.PlotWidget(name="mystery", pen=(0,0,255),
                                         background=None)
        self.plot.setStyleSheet("background: transparent;")

        result = scene.addWidget(self.plot)
        result.setParentItem(self)
        self.plot.setGeometry(QtCore.QRect(32, 333-291, 668, 270))

        self.add_main_title(title, self)

        icon_filename = ":ui/default_icon.png"
        self.add_main_icon(icon_filename, self)

        self.minimum = SmallTextBox(prefix="MIN:")
        self.minimum.setPos(706, 333-233)
        self.minimum.setParentItem(self)

        self.maximum = SmallTextBox(prefix="MAX:", val="987.65")
        self.maximum.setPos(706, 333-164)
        self.maximum.setParentItem(self)


        self.fps = SmallTextBox(prefix="FPS:", val="9999")
        self.fps.setPos(706, 333-95)
        self.fps.setParentItem(self)

        prefix = ":ui/toggle_button_"
        self.pause_button = ToggleButton(prefix=prefix)
        self.pause_button.setPos(706, 333-289)
        self.pause_button.setParentItem(self)

    def add_main_icon(self, filename, parent):
        """ Add a graphical indicator pixmap to the title area.
        """
        # The icon to the left of the main title
        self.icon = QtGui.QGraphicsPixmapItem(filename)
        self.icon.setPos(33, 13)
        self.icon.setParentItem(parent)

    def add_main_title(self, title, parent):
        """ Add a text item with drop shadow.
        """

        # Filename will work on linux, actual font name with spaces is
        # required for success on windows
        self.default_font = QtGui.QFont("Gears of Peace")
        self.default_font.setPointSize( 12 )

        white = QtGui.QColor(255, 255, 255, 255)
        self.title = QtGui.QGraphicsSimpleTextItem(title)
        self.title.setPos(65, 14)
        self.title.setBrush(white)
        self.title.setParentItem(parent)
        self.title.setFont(self.default_font)

        self.shadow = QtGui.QGraphicsDropShadowEffect()
        self.shadow.setOffset(2, 2)
        self.title.setGraphicsEffect(self.shadow)

class ToggleButton(QtGui.QGraphicsPixmapItem):
    """ Switch foreground pixmap elements to indicate toggled states.
    """
    def __init__(self, designator="default",
                 prefix=":ui/toggle_button_"):
        self.activated = "%s%s.png" % (prefix, "activated")
        self.deactivated = "%s%s.png" % (prefix, "deactivated")
        super(ToggleButton, self).__init__(self.activated)

        self._state = "play"
        print "startup with: %s" % self._state

        self.shadow = QtGui.QGraphicsDropShadowEffect()
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 128))
        self.shadow.setOffset(2, 2)
        self.setGraphicsEffect(self.shadow)

    @property
    def state(self):
        return self._state

    def mousePressEvent(self, event):
        log.debug("you pressed %s", event.pos())
        if self._state == "play":
            self._state = "pause"
            self.setPixmap(self.deactivated)
        else:
            self._state = "play"
            self.setPixmap(self.activated)

class SmallTextBox(QtGui.QGraphicsPixmapItem):
    """ Designed to display an abbreviated text description and a %3.2f
    formatted value.
    """
    def __init__(self, prefix="Min", val="123.45",
                 filename="small_number_designator_export.png"):

        full_path = ":ui/%s" % filename
        super(SmallTextBox, self).__init__(full_path)

        white = QtGui.QColor(255, 255, 255, 255)
        self.prefix_font = QtGui.QFont("Gears of Peace")
        self.prefix_font.setPointSize(7)

        self.prefix = QtGui.QGraphicsSimpleTextItem(prefix)
        self.prefix.setPos(5, 5)
        self.prefix.setBrush(white)
        self.prefix.setParentItem(self)
        self.prefix.setFont(self.prefix_font)

        self.value_font = QtGui.QFont("Gears of Peace")
        self.value_font.setPointSize(8)
        self.value = QtGui.QGraphicsSimpleTextItem(val)
        self.value.setPos(4, 22)
        self.value.setBrush(white)
        self.value.setParentItem(self)
        self.value.setFont(self.value_font)

        self.shadow = QtGui.QGraphicsDropShadowEffect()
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 128))
        self.shadow.setOffset(2, 2)
        self.setGraphicsEffect(self.shadow)

    @property
    def text(self):
        return self.value.text()

    def setText(self, new_text):
        self.value.setText(str(new_text))
