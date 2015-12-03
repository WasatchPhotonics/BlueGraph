""" NonBlockingWrapper - classes to use multiprocessing to turn blocking
simulation and real devices into non-blocking variants. This is designed
to support separate acquisition and visualization chains, as well as long
integration times of camera devices.
"""

import Queue
import logging
import multiprocessing

from bluegraph.devices import Simulation

log = logging.getLogger(__name__)

class Wrapper(object):
    """ Expose the same interface as a simulated temperature device.
    Wrap the actual device calls in a multiprocessing class.
    """
    def __init__(self):
        super(Wrapper, self).__init__()
        log.debug("In wrapper")

        self.control_queue = multiprocessing.Queue()
        self.read_queue = multiprocessing.Queue()

        mp = multiprocessing.Process
        log.info("Start process")
        self.process = mp(target=self.temp_reader,
                          args=(self.device, self.read_queue,
                                self.control_queue)
                         )
        self.process.start()

    def temp_reader(self, device, data_queue, control_queue):
        """ multiprocessing function call
        """
        self.device = Simulation.SimulatedTemperature()
        if not self.device.connect():
            log.critical("Problem connecting to device")
            return False

        self.read_queue.put(123.00)
        self.control_queue.put("ACQUIRE")

        continue_reading = True
        while(continue_reading):
            log.debug("At command read")
            command = None
            try:
                command = control_queue.get_nowait()
                log.debug("Command: %s", command)
            except Queue.Empty:
                pass
            except Exception as exc:
                log.critical("Control queue exception: %s", exc)

            if command == "STOP":
                continue_reading = False
            else:
                reading = device.read()
                data_queue.put(reading)
                log.debug("Add reading: %s", reading)

        log.debug("Exit reader")

    def connect(self):
        self.control_queue.put("CONNECT")
        return True

    def disconnect(self):
        log.debug("Wrapper disconnect")
        self.control_queue.put("DISCONNECT")
        self.process.join()
        return True

    def read(self):
        result = None
        try:
            result = self.read_queue.get_nowait()
            log.debug("Get result: %s", result)
            self.control_queue.put("ACQUIRE")

        except Queue.Empty:
            #log.debug("Empty queue")
            pass

        except Exception as exc:
            log.critical("Unknown error: %s", exc)

        return result
