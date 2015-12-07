""" Simulation devices for bluegraph visualizations
"""

import time
import numpy
import random
import logging
import Queue
import multiprocessing

log = logging.getLogger(__name__)

class SimulatedDevice(object):
    """ Base class api definition for device read simulations. Inherit from
    this device and reimplment the functions below to communicate with
    actual devices.
    """
    def __init__(self):
        super(SimulatedDevice, self).__init__()
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


class SimulatedSpectra(SimulatedDevice):
    """ Return the specified number of pixels with randomized peaks for
    use in test visualizations.
    """
    def __init__(self, pixel_width=1024):
        super(SimulatedSpectra, self).__init__()
        log.debug("Simulated Spectra")
        self.pixel_width = pixel_width

    def read(self):
        """ Return simulated data. Generate the noise applied waveform
        then sleep the remainder of the time to lock the return of data
        to once every N ms.
        """
        cue_time = time.time()
        nru = numpy.random.uniform
        noise_data = nru(1, 65535, self.pixel_width)
        return noise_data

class RegulatedSpectra(SimulatedSpectra):
    """ Enforce a minimum time delay for every read.
    """
    def read(self):
        cue_time = time.time()
        result = super(RegulatedSpectra, self).read()
        end_time = time.time()

        time_diff = end_time - cue_time
        if time_diff < 0.2:
            time.sleep(0.2 - time_diff)

        return result


class BlockingInterface(object):
    """ Wrap the defined device in a separate process. Use queues to
    request and emit data in lock step to create a blocking interface.
    """
    def __init__(self, device_type="SimulatedDevice"):
        super(BlockingInterface, self).__init__()

        self.device_type = device_type
        self.data_queue = multiprocessing.Queue()
        self.control_queue = multiprocessing.Queue()

        mp = multiprocessing.Process
        args = (self.control_queue, self.data_queue)
        self.process = mp(target=self.worker, args=args)
        self.process.start()

    def worker(self, control_queue, data_queue):
        """ While the stop command poison pill is not received, read
        commands from the control queue. Connect, disconnect and read
        data from the device as specified.
        """
        continue_loop = True
        self.device = None

        while(continue_loop):
            command = control_queue.get()

            if command == "CONNECT":
                log.info("Setup: %s", self.device_type)
                if self.device_type == "SimulatedDevice":
                    self.device = SimulatedDevice()
                elif self.device_type == "SimulatedSpectra":
                    self.device = SimulatedSpectra()
                elif self.device_type == "RegulatedSpectra":
                    self.device = RegulatedSpectra()

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
        """ Add the connection command to the queue.
        """
        result = self.queue_command("CONNECT", "connect_successful")
        return result

    def queue_command(self, command, success):
        """ Respect the simple device interface by issuing commands on the
        control queue. Wait for a response on the data queue for lock step
        control.
        """
        self.control_queue.put(command)
        status = self.data_queue.get()
        if status == success:
            return True

        log.critical("Command %s problem: %s", command, status)
        return False

    def disconnect(self):
        """ Add the disconnection command to the queue, terminate any
        running processes.
        """
        log.info("Add disconnect to queue")
        result = self.queue_command("DISCONNECT", "disconnect_successful")

        # Always exit the processes, event if disconnect fails
        self.process.join()
        return result

    def read(self):
        """ Add the acquire command to the control queue, then do a
        blocking wait on the data queue.
        """
        self.control_queue.put("ACQUIRE")
        result = self.data_queue.get()
        return result

class NonBlockingInterface(BlockingInterface):
    """ Wrapper around the blocking interface that allows for immediate
    empty queue returns of the data queue. Use this in applications that
    need better responsivity by continuously calling read(), and sleep
    when the response is None.
    """
    def __init__(self, device_type="SimulatedDevice"):
        self.device_type = device_type
        super(NonBlockingInterface, self).__init__(device_type=device_type)

        self.acquire_sent = False # Wait for an acquire to complete

    def send_acquire(self):
        """ Only send one acquire onto the control queue at a time.
        Requires that the removal of the data from the data queue resets
        the acquire_sent parameter. Apparently python 2.7.x on MS windows
        blocks somehow on the queue.empty call. Replace with an attempted
        non blocking get.
        """
        if self.acquire_sent:
            return

        # See notes above on why queue.empt() is not used.
        queue_empty = True
        try:
            result = self.control_queue.get_nowait()
            result = False
        except Queue.Empty:
            log.debug("Queue is empty")
        except Exception as exc:
            log.critical("Unknown exception")

        if queue_empty == True:
            self.control_queue.put("ACQUIRE")
            self.acquire_sent = True

    def read(self):
        """ Send an acquire command on the control queue. Immediately
        attempt to retrieve data from the data queue, returning a None
        when the data queue is empty.
        """
        self.send_acquire()

        result = None
        try:
            result = self.data_queue.get_nowait()
            self.acquire_sent = False

        except Queue.Empty:
            log.debug("empty queue")

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
