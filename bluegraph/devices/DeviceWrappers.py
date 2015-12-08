""" Simulation devices for bluegraph visualizations
"""

import time
import numpy
import random
import logging
import Queue
import multiprocessing

from collections import deque

from bluegraph.devices import Simulation

log = logging.getLogger(__name__)

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
                    self.device = Simulation.SimulatedDevice()

                elif self.device_type == "SimulatedSpectra":
                    self.device = Simulation.SimulatedSpectra()

                elif self.device_type == "RegulatedSpectra":
                    self.device = Simulation.RegulatedSpectra()

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

        # See notes above on why queue.empty() is not used.
        queue_empty = True
        try:
            result = self.control_queue.get_nowait()
        except Queue.Empty:
            log.debug("Queue is empty")
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


