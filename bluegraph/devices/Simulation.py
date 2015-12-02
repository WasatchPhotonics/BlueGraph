""" Simulation devices for bluegraph visualizations
"""

import time
import numpy
import random
import logging

log = logging.getLogger(__name__)

class SimulatedLaserPowerMeter(object):
    """ Provide a Thorlabs pm100usb encapsulation of typical values seen
    on a Wasatch Photonics 785LM laser spectrometer.
    """
    def __init__(self):
        super(SimulatedLaserPowerMeter, self).__init__()
        log.info("init device")
        self._hardware_list = ["Simulated PM100"]
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
        return self._hardware_list

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

class SimulatedSpectra(SimulatedLaserPowerMeter):
    """ Return the specified number of pixels with randomized peaks for
    use in test visualizations.
    """
    def __init__(self, pixel_width=1024):
        super(SimulatedSpectra, self).__init__()
        log.debug("Simulated Spectra")
        self._hardware_list = ["Simulated Spectra"]
        self.pixel_width = pixel_width

    def read(self):
        """ Return simulated data. Generate the noise applied waveform
        then sleep the remainder of the time to lock the return of data
        to once every N ms.
        """

        start_time = time.time()
        nru = numpy.random.uniform
        noise_data = nru(10, 20, self.pixel_width)

        time_diff = start_time - time.time()
        if time_diff < 0.005:
            time_wait = 0.005 - abs(time_diff)
            #print "force sleep: %s %s" % (time_diff, time_wait)
            time.sleep(abs(time_wait))

        return noise_data

