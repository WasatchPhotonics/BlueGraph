""" Simulation devices for bluegraph visualizations
"""

import time
import numpy
import random
import logging
import Queue
import multiprocessing

from collections import deque

log = logging.getLogger(__name__)

class SimulatedDevice(object):
    """ Base class api definition for device read simulations. Inherit
    from this device and reimplment the functions below to communicate
    with actual devices.
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


class RegulatedDevice(SimulatedDevice):
    """ Enforce a minimum time delay for every read.
    """
    def read(self):
        cue_time = time.time()
        result = super(RegulatedDevice, self).read()
        end_time = time.time()

        time_diff = end_time - cue_time
        if time_diff < 0.2:
            time.sleep(0.2 - time_diff)

        return result

class StripChartDevice(RegulatedDevice):
    """ Return a list of readings up to the maximum size. Automatically
    roll the list when it has been filled.
    """
    def __init__(self, size=20):
        super(StripChartDevice, self).__init__()
        self.size = size
        self.history = deque()

    def read(self):
        """ Read and add to list, then roll.
        """

        result = super(StripChartDevice, self).read()
        self.history.append(result[0])

        if len(self.history) > self.size:
            self.history.popleft()

        #print("History is %s", self.history)
        return self.history



class SimulatedSpectra(SimulatedDevice):
    """ Return the specified number of pixels with randomized peaks for
    use in test visualizations.
    """
    def __init__(self, pixel_width=1024):
        super(SimulatedSpectra, self).__init__()
        log.debug("Simulated Spectra width %s", pixel_width)
        print("Simulated Spectra width %s", pixel_width)
        self.pixel_width = pixel_width

    def read(self):
        """ Return simulated data. Generate the noise applied waveform
        as fast as possible. This is a fairly cpu intensive random
        number generation process, depending on pixel width. This is
        designed for testing the blocking and non blocking wrappers.
        """
        cue_time = time.time()
        nru = numpy.random.uniform
        noise_data = nru(123, 65500, self.pixel_width)

        # Enforce the first and last for min/max tests
        noise_data[0] = 100
        noise_data[-1] = 65535
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
