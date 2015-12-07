""" BlueGraph - application control for visualization of data.
"""

import sys
import logging
import argparse

from PySide import QtGui, QtCore

from bluegraph import control

logging.basicConfig(filename="BlueGraph_log.txt", filemode="w",
                    level=logging.DEBUG)
log = logging.getLogger()

strm = logging.StreamHandler(sys.stderr)
frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
strm.setFormatter(frmt)
log.addHandler(strm)
log.setLevel(logging.INFO)

import signal
def signal_handler(signal, frame):
        log.critical('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

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
        #self.control = control.BlueGraphController("SimulatedSpectra")
        self.control = control.BlueGraphController("NonBlockingSimulatedSpectra")
        self.control.control_exit_signal.exit.connect(self.closeEvent)
        sys.exit(app.exec_())

    def closeEvent(self):
        """ catch the exit signal from the control application, and
        call qapplication Quit. This will prevent hangs on exit.
        """
        log.debug("Close event")
        QtGui.QApplication.quit()

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
