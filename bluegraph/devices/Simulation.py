""" Simulation devices for bluegraph visualizations
"""

import time
import numpy
import random
import logging
import Queue
import multiprocessing


log = logging.getLogger(__name__)

class SimulatedTemperature(object):
    """ Base class api definition for blocking device read simulations.
    """
    def __init__(self):
        super(SimulatedTemperature, self).__init__()
        self.connected = False
        self.base_value = 100.00

    def connect(self):
        self.connected = True
        return True

    def disconnect(self):
        self.connected = False
        return True

    def read(self):
        """ Return a randomized value plus a baseline
        """
        noise = numpy.random.uniform(0, 99, 1)
        value = self.base_value + (noise / 100.0)
        time.sleep(0.10)
        return value

class BlockingInterface(object):
    def __init__(self):
        super(BlockingInterface, self).__init__()

        self.data_queue = multiprocessing.Queue()
        self.control_queue = multiprocessing.Queue()

        mp = multiprocessing.Process
        self.process = mp(target=self.worker,
                          args=(self.control_queue, self.data_queue)
                         )
        self.process.start()

    def worker(self, control_queue, data_queue):
        continue_loop = True
        self.device = None
        while(continue_loop):
            command = control_queue.get()
            response = None
            if command == "CONNECT":
                self.device = SimulatedTemperature()
                self.device.connect()
                response = "connect_successful"

            elif command == "DISCONNECT":
                self.device.disconnect()
                continue_loop = False
                response = "disconnect_successful"

            else:
                response = self.device.read()

            data_queue.put(response)


    def connect(self):
        self.control_queue.put("CONNECT")
        status = self.data_queue.get()
        if status == "connect_successful":
            return True

        log.critical("Problem connecting %s", status)
        return False

    def disconnect(self):
        self.control_queue.put("DISCONNECT")
        status = self.data_queue.get()
        if status == "disconnect_successful":
            return True

        log.critical("Problem disconnecting %s", status)
        self.process.join()
        return False

    def read(self):
        self.control_queue.put("ACQUIRE")
        result = self.data_queue.get()
        return result

class NonBlockingInterface(BlockingInterface):
    def __init__(self):
        super(NonBlockingInterface, self).__init__()

    def read(self):
        result = None
        try:
            if self.control_queue.empty():
                self.control_queue.put("ACQUIRE")
            result = self.data_queue.get_nowait()
        except Queue.Empty:
            log.debug("empty queue")
        except Exception as exc:
            log.critical("Unknown exception: %s", exc)

        return result



class SimulatedLaserPowerMeter(object):
    """ Provide a Thorlabs pm100usb encapsulation of typical values seen
    on a Wasatch Photonics 785LM laser spectrometer.
    """
    def __init__(self):
        super(SimulatedLaserPowerMeter, self).__init__()
        log.info("init device")
        self._open = False
        self.wait_interval = 0.100
        self.last_val = 110

    def is_open(self):
        """ Convenience function to return the internally tracked device
        open status.
        """
        return self._open

    def close(self):
        """ Force the device to close, record the is open state.
        """
        log.info("Close device")
        self._open = False

    def list_hardware(self):
        """ Provide a list of available devices.
        """
        return ["Simulated PM100"]

    def connect(self, serial=None):
        """ Connect to the first device in the list if none specified.
        """
        if serial == None:
            serial = self.list_hardware()[0]
        self._open = True
        return self._open

    def read(self):
        """ Perform a simulated read from the device, respecting
        assigned rates of update. Start at 111, and roll the major power
        meter read when greater than 115. Add random hundredths.
        """
        time.sleep(self.wait_interval)
        val = self.last_val
        val += 1
        if val > 115:
            val = 110
        self.last_val = val

        val += random.random()
        log.info("Read: %s", val)
        return val
