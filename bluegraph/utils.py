""" linegrab utils - classes and helper functions for the linegrab
application.
"""

try:
    from PyQt4.QtCore import QTimer
except ImportError:
    from PySide.QtCore import QTimer
    

def load_style_sheet(filename):
    """ Load the qss stylesheet into a string suitable for passing
    to the main widget.
    """
    qss_file = open("linegrab/ui/%s" % filename)
    temp_string = ""
    for line in qss_file.readlines():
        temp_string += line

    return temp_string

class SimpleFPS(object):
    """ Use qtimer and a tick function to return the number of ticks
    returned for a simple FPS computation.
    """
    def __init__(self):
        super(SimpleFPS, self).__init__()
        self.fps = -1
        self.ticks = 0

        self.fps_timer = QTimer()
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
