""" unit and functional tests for bluegraph application.
"""

import time
from bluegraph.devices import Simulation

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
