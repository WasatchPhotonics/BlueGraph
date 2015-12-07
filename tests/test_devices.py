""" unit and functional tests for bluegraph application.
"""
import sys
import time
import numpy
import logging

from bluegraph.devices import Simulation


log = logging.getLogger()

strm = logging.StreamHandler(sys.stderr)
frmt = logging.Formatter("%(name)s - %(levelname)s %(message)s")
strm.setFormatter(frmt)
log.addHandler(strm)
log.setLevel(logging.DEBUG)

class TestSimulatedDevice:
    def test_connect_and_disconnect_status_track(self):
        device = Simulation.SimulatedDevice()
        assert device.connect() == True
        assert device.connected == True

        device.disconnect()
        assert device.connected == False

    def test_data_stream_is_random(self):
        device = Simulation.SimulatedDevice()
        device.connect()
        first = device.read()
        assert first != device.read()

    def test_data_stream_is_speed_locked(self):
        device = Simulation.SimulatedDevice()
        device.connect()

        start_time = time.time()
        for i in range(10):
            device.read()
        end_time = time.time()

        time_diff = end_time - start_time
        assert time_diff > 0.9
        assert time_diff < 1.1

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


class TestMultiProcessingSimulation:
    def test_connect_and_disconnect_close_effectively(self):
        block = Simulation.BlockingInterface()
        assert block.connect() == True
        assert block.disconnect() == True

    def test_blocking_returns_random_data(self):
        block = Simulation.BlockingInterface()
        block.connect()
        first = block.read()
        second = block.read()
        block.disconnect()

        assert first != second

    def test_blocking_data_stream_is_time_locked(self):
        block = Simulation.BlockingInterface()
        assert block.connect() == True

        start_time = time.time()
        for i in range(10):
            block.read()
        assert block.disconnect() == True
        end_time = time.time()

        time_diff = end_time - start_time
        assert time_diff > 0.9
        assert time_diff < 1.1

    def test_nonblocking_returns_random_data(self):
        log.info("NBLK setup")
        nblk = Simulation.NonBlockingInterface()

        log.info("NBLK connect")
        nblk.connect()

        log.info("NBLK pre-read")
        first = nblk.read()

        while first is None:
            log.info("NBLK loop-read")
            first = nblk.read()

        #second = nblk.read()
        #while second is None:
            #second = nblk.read()

        log.info("NBLK disconnect")
        nblk.disconnect()
        assert first != second

    def test_nonblocking_data_stream_is_not_time_locked(self):
        nblk = Simulation.NonBlockingInterface()
        nblk.connect()

        start_time = time.time()
        for i in range(200):
            nblk.read()
        end_time = time.time()

        time_diff = end_time - start_time
        assert time_diff <= 1.0
        nblk.disconnect()

    def test_nonblocking_wait_for_data_is_time_locked(self):
        nblk = Simulation.NonBlockingInterface()
        nblk.connect()
        start_time = time.time()
        for i in range(10):
            result = nblk.read()
            while result is None:
                result = nblk.read()
        end_time = time.time()

        time_diff = end_time - start_time
        assert time_diff >= 0.9
        assert time_diff <= 1.1

        nblk.disconnect()

class TestSimulatedSpectra:
    def test_connect_disconnect(self):
        device = Simulation.SimulatedSpectra()
        assert device.connect() == True
        assert device.connected == True

        device.disconnect()
        assert device.connected == False

    def test_data_stream_is_randomized(self):
        device = Simulation.SimulatedSpectra()
        device.connect()
        first = device.read()
        second = device.read()
        assert numpy.array_equal(first, second) == False
        device.disconnect()

    def test_stream_data_is_specified_pixels_width(self):
        device = Simulation.SimulatedSpectra()
        device.connect()
        assert len(device.read()) == 1024
        device.disconnect()

        device = Simulation.SimulatedSpectra(pixel_width=2048)
        device.connect()
        assert len(device.read()) == 2048
        device.disconnect()

class TestRegulatedSpectra:
    def test_stream_data_is_time_regulated(self):
        device = Simulation.RegulatedSpectra()
        assert device.connect() == True

        start_time = time.time()
        total_reads = 0
        for i in range(10):
            total_reads += 1
            result = device.read()
        cease_time = time.time()

        time_diff = cease_time - start_time
        assert time_diff >= 1.9
        assert time_diff <= 2.1
        assert total_reads == 10

        assert device.disconnect() == True

    def test_nonblocking_regulated_stream_data(self):
        device = Simulation.NonBlockingInterface("RegulatedSpectra")
        assert device.connect() == True

        # Total reads should be vastly higher than the requested reads
        # as the non blocking queue get should return almost instantly
        start_time = time.time()
        total_reads = 0
        for i in range(10):
            total_reads += 1
            result = device.read()
            while result is None:
                total_reads += 1
                result = device.read()
        cease_time = time.time()

        time_diff = cease_time - start_time
        log.info("total reasd: %s", total_reads)
        assert total_reads > 1000
        assert time_diff >= 1.9
        assert time_diff <= 2.1

        assert device.disconnect() == True

