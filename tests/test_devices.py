""" unit and functional tests for bluegraph application.
"""

import zmq
import time
import numpy

from bluegraph.devices import Simulation
from bluegraph.devices import ZMQWrapper

class TestSimulatedLaserPowerMeter:
    def test_list_hardware_returns_simulated_device(self):
        device = Simulation.SimulatedLaserPowerMeter()
        dev_list = device.list_hardware()
        dev_str = "Simulated PM100"
        assert dev_str == dev_list[0]

    def test_connect_simulated_device_returns_ok(self):
        device = Simulation.SimulatedLaserPowerMeter()
        assert device.connect() == True
        assert device.is_open() == True

        device.close()
        assert device.is_open() == False

    def test_get_stream_returns_10_reads_per_second(self):
        device = Simulation.SimulatedLaserPowerMeter()
        device.connect()

        start_time = time.time()
        for i in range(10):
            device.read()
        end_time = time.time()

        time_diff = end_time - start_time
        assert time_diff < 1.1
        assert time_diff > 0.9

    def test_stream_data_is_randomized(self):
        device = Simulation.SimulatedLaserPowerMeter()
        device.connect()
        first = device.read()
        assert first != device.read()

class TestSimulatedSpectra:
    def test_spectra_stream_returns_expected_reads_per_second(self):
        device = Simulation.SimulatedSpectra()
        device.connect()

        start_time = time.time()
        for i in range(200):
            device.read()
        end_time = time.time()

        time_diff = end_time - start_time
        print "Actual diff %s" % time_diff
        assert time_diff < 1.1
        assert time_diff > 0.9

    def test_stream_data_is_randomized(self):
        device = Simulation.SimulatedSpectra()
        device.connect()
        first = device.read()
        assert numpy.array_equal(first, device.read()) == False

    def test_stream_data_is_specified_width_in_pixels(self):
        device = Simulation.SimulatedSpectra()
        device.connect()
        assert len(device.read()) == 1024

        device = Simulation.SimulatedSpectra(2048)
        device.connect()
        assert len(device.read()) == 2048


class TestZMQSimulationWrapper:

    def test_connect_to_publisher(self):
        return
        pub_wrap = ZMQWrapper.Publisher("SimulatedLaserPower")

        temp_context = zmq.Context()
        temp_socket = temp_context.socket(zmq.SUB)
        temp_socket.connect ("tcp://127.0.0.1:5678")
        temp_socket.setsockopt(zmq.SUBSCRIBE, "SimulatedLaserPower")
        pub_wrap.close()

    def test_subscribed_events_return_blind_data(self):
        return
        temp_context = zmq.Context()
        temp_socket = temp_context.socket(zmq.SUB)
        temp_socket.connect ("tcp://127.0.0.1:5678")
        temp_socket.setsockopt(zmq.SUBSCRIBE, "SimulatedLaserPower")

        print "start pub"
        pub_wrap = ZMQWrapper.Publisher("SimulatedLaserPower", 1)
        result = temp_socket.recv()
        print "Full result %s" % result
        topic, message_data = result.split(",")
        assert topic == "SimulatedLaserPower"
        assert message_data != -1.0
        pub_wrap.close()

    def test_returns_specified_number_of_publish_events(self):
        return
        temp_context = zmq.Context()
        temp_socket = temp_context.socket(zmq.SUB)
        temp_socket.connect ("tcp://127.0.0.1:5678")
        temp_socket.setsockopt(zmq.SUBSCRIBE, "SimulatedLaserPower")

        pub_wrap = ZMQWrapper.Publisher("SimulatedLaserPower", 10)

        # Read 10 events expected
        for i in range(10):
            result = temp_socket.recv()
            topic, message_data = result.split(",")
            assert topic == "SimulatedLaserPower"
            assert message_data != -1.0

        # Expect a timeout failure on the next read
        try:
            temp_socket.RCVTIMEO = 1000
            result = temp_socket.recv()
            assert result == None
        except Exception as exc:
            print "Exception: %s" % exc
        pub_wrap.close()

    def test_returns_data_at_expected_rate(self):
        return
        temp_context = zmq.Context()
        temp_socket = temp_context.socket(zmq.SUB)
        temp_socket.connect ("tcp://127.0.0.1:5678")
        temp_socket.setsockopt(zmq.SUBSCRIBE, "SimulatedLaserPower")

        pub_wrap = ZMQWrapper.Publisher("SimulatedLaserPower", 10)

        print "Start read in range"
        start_time = time.time()
        for i in range(10):
            result = temp_socket.recv()
            print "Read: %s" % i
        end_time = time.time()

        time_diff = end_time - start_time
        #print "time diff is: %s" % time_diff
        # One second for delay setup, one second for socket connection, and one
        # second for the actual reads?
        assert time_diff < 3.1
        assert time_diff > 2.9


