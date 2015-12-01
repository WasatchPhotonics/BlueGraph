""" ZMQ Wrapper around real and simulation devices for bluegraph
visualizations.
"""

import zmq
import time
import logging
import multiprocessing

from bluegraph.devices import Simulation

log = logging.getLogger(__name__)

class Publisher(object):
    """ Provide a tcp publisher socket for readings from the specified
    device.
    """
    def __init__(self, device=None, max_publish=None):
        super(Publisher, self).__init__()

        self.max_publish = max_publish
        self._device_name = device
       
        self.device = Simulation.SimulatedLaserPowerMeter() 
        self.device.connect()
        print "Pre continuous"
       
        self.emit_proc = multiprocessing.Process(target=self.emit_continuously)
        self.emit_proc.start()

    def emit_continuously(self, interval=0.500):
        """ Every interval wall clock seconds, emit a message on the
        publisher queue.
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:5678")
        time.sleep(1) # required to let the subscriber connect
       
        while(self.max_publish > 0): 
            str_mesg = "%s, %s" % (self._device_name, self.device.read())
            log.debug("send: %s", str_mesg) 
            print("send: %s" % str_mesg) 
            self.socket.send(str_mesg)

            time.sleep(interval)
            self.max_publish -= 1
