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

class DeviceChooser(object):
    """ Convert the string specification to an importable module. This is
    to define the classes at runtime, so you can add in new modules for
    display that may not have a testable portion in a CI environment. See
    Phidgeter for examples.
    """
    def __init__(self):
        pass

    def create(self, device_class, device_type, device_args=None):
        """ Create a device from the bluegraph modules available. Certain
        modules will only be available at runtime, so attempt to import
        them during the creation process. This gets really ugly when
        passing arguments as well. There has to be a more maintainable
        way to do this.

        This approach permits the importing of straight device modules
        like: Simulation.RegulatedSpectra. As well as the import of the
        wrapper modules like Blocking.RegulatedSpectra
        """
        try:
            cmd_name = "bluegraph.devices.%s" % device_class
            from_list = "bluegraph.devices"
            command_module = __import__(cmd_name, fromlist=from_list)
        except ImportError as exc:
            print "Exception importing %s" % exc


        # This is ugly - there has to be a more pythonic way to do this

        # command_module is the module name, like Simulation or Phidgeter
        # Append the class name like NonBlocking
        cmd_str = "command_module.%s" % device_type

        # Pass in the argument string like "RegulatedDevice" if it exists
        if device_args is not None:
            cmd_str = cmd_str + "(\"%s\")" % device_args
        else:
            cmd_str = cmd_str + "()"

        print "Attempt to import: %s" % cmd_str
        device = eval(cmd_str)

        return device



class BlockingInterface(object):
    """ Wrap the defined device in a separate process. Use queues to
    request and emit data in lock step to create a blocking interface.
    """
    def __init__(self, device_type="Simulation.SimulatedDevice"):
        print "Blocking create type: %s" % device_type
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
                log.info("NB Setup: %s", self.device_type)
                print("NB Setup: %s", self.device_type)
                self.device = self.create_device()

                self.device.connect()
                response = "connect_successful"

            elif command == "DISCONNECT":
                self.device.disconnect()
                continue_loop = False
                response = "disconnect_successful"

            else:
                response = self.device.read()

            data_queue.put(response)

    def create_device(self):
        """ Use eval to import the specified module.
        """
        (bg_module, bg_class) = self.device_type.split(".")
        try:
            cmd_name = "bluegraph.devices.%s" % bg_module
            from_list = "bluegraph.devices"
            command_module = __import__(cmd_name, fromlist=from_list)
        except ImportError as exc:
            print "BG Exception importing %s" % exc

        cmd_str = "command_module.%s" % bg_class
        cmd_str = cmd_str + "()"

        print "BG Attempt to import: %s" % cmd_str
        device = eval(cmd_str)

        return device




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
    def __init__(self, device_type="Simulation.SimulatedDevice"):
        self.device_type = device_type
        print "non blocking create with: %s" % device_type
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


