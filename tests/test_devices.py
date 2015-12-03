""" unit and functional tests for bluegraph application.
"""
import sys
import time
import logging

from bluegraph.devices import Simulation
from bluegraph.devices import NonBlockingWrapper


log = logging.getLogger()

strm = logging.StreamHandler(sys.stderr)
frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
strm.setFormatter(frmt)
log.addHandler(strm)
log.setLevel(logging.DEBUG)

class TestSimulatedTemperature:
    def test_connect_and_disconnect_status_track(self):
        device = Simulation.SimulatedTemperature()
        assert device.connect() == True
        assert device.connected == True

        device.disconnect()
        assert device.connected == False

    def test_data_stream_is_random(self):
        device = Simulation.SimulatedTemperature()
        device.connect()
        first = device.read()
        assert first != device.read()

    def test_data_stream_is_speed_locked(self):
        device = Simulation.SimulatedTemperature()
        device.connect()

        start_time = time.time()
        for i in range(10):
            device.read()
        end_time = time.time()

        time_diff = end_time - start_time
        assert time_diff > 0.9
        assert time_diff < 1.1

class TestNonBlockingWrapper:
    def test_connect_exposes_same_read_interface(self):
        wrapper = NonBlockingWrapper.Wrapper()
        assert wrapper.connect() == True
        assert wrapper.connected == True

        wrapper.disconnect()
        assert wrapper.connected == False

    def test_data_stream_is_randomized(self):
        wrapper = NonBlockingWrapper.Wrapper()
        wrapper.connect()
        first = wrapper.read()
        while first is None:
            first = wrapper.read()

        second = wrapper.read()
        while second is None:
            second = wrapper.read()

        wrapper.disconnect()
        assert first != second

    def test_data_stream_is_not_speed_locked(self):
        wrapper = NonBlockingWrapper.Wrapper()
        wrapper.connect()

        # These 100 reads should return close to instantly because
        # queue read is non blocking
        start_time = time.time()
        for i in range(100):
            wrapper.read()
        end_time = time.time()

        wrapper.disconnect()
        time_diff = end_time - start_time
        assert time_diff < 0.1

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
