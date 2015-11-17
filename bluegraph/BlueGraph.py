""" BlueGraph - application control for visualization of data.
"""

import sys
import logging
import argparse

from PySide import QtGui, QtCore

# This should really be controller import, which in turn loads the views
from bluegraph import views

logging.basicConfig(filename="BlueGraph_log.txt", filemode="w",
                    level=logging.DEBUG)
log = logging.getLogger()

strm = logging.StreamHandler(sys.stderr)
frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
strm.setFormatter(frmt)
log.addHandler(strm)
log.setLevel(logging.DEBUG)

class BlueGraphApplication(object):
    """ Create the window with the graphs, setup communication based on
    the specified device.
    """
    def __init__(self):
        super(BlueGraphApplication, self).__init__()
        log.debug("startup")
        self.parser = self.create_parser()
        self.form = None
        self.args = None

    def parse_args(self, argv):
        """ Handle any bad arguments, then set defaults.
        """
        log.debug("Process args: %s", argv)
        self.args = self.parser.parse_args(argv)
        return self.args

    def create_parser(self):
        """ Create the parser with arguments specific to this
        application.
        """
        desc = "acquire from specified device, display line graph"
        parser = argparse.ArgumentParser(description=desc)

        help_str = "Automatically terminate the program for testing"
        parser.add_argument("-t", "--testing", action="store_true",
                            help=help_str)
        return parser

    def run(self):
        """ This is the application code that is called by the main
        function. The architectural idea is to have as little code in
        main as possible and create the qapplication here so the
        nosetests can function. Only create the application if not using
        the unittest generated controller.
        """
        app = QtGui.QApplication([])
        self.delay_close()

        #self.form = views.Basic()
        self.form = views.BasicSVG()

        sys.exit(app.exec_())

    def delay_close(self):
        """ For testing purposes, create a qtimer that triggers the
        close event after a delay.
        """
        log.debug("Trigger delay close")
        self.close_timer = QtCore.QTimer()
        self.close_timer.timeout.connect(self.closeEvent)
        self.close_timer.start(5000)

    def closeEvent(self):
        # .quit required for test cases to exit 
        QtGui.QApplication.quit()
        #event.accept()


def main(argv=None):
    """ main calls the wrapper code around the application objects with
    as little framework as possible. See:
    https://groups.google.com/d/msg/comp.lang.python/j_tFS3uUFBY/\
        ciA7xQMe6TMJ
    """
    argv = argv[1:]
    log.debug("Arguments: %s", argv)

    exit_code = 0
    print "Application exec"
    try:
        go_app = BlueGraphApplication()
        go_app.parse_args(argv)
        go_app.run()

    except SystemExit, exc:
        exit_code = exc.code

    return exit_code

if __name__ == "__main__":
    sys.exit(main(sys.argv))
