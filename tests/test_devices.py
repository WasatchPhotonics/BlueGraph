""" unit and functional tests for bluegraph application.
"""

import zmq
import time

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

class TestZMQSimulationWrapper:
    def test_wrapper_creation_exposes_publisher(self):
        pub_wrap = ZMQWrapper.Publisher("SimulatedLaserPower")
        assert isinstance(pub_wrap.context, zmq.Context)
        assert isinstance(pub_wrap.socket, zmq.Socket)

    def test_connect_to_publisher(self):
        pub_wrap = ZMQWrapper.Publisher("SimulatedLaserPower")

        temp_context = zmq.Context()
        temp_socket = temp_context.socket(zmq.SUB)
        temp_socket.connect ("tcp://127.0.0.1:5678")
        temp_socket.setsockopt(zmq.SUBSCRIBE, "SimulatedLaserPower")

    def test_subscribed_events_return_blind_data(self):
        temp_context = zmq.Context()
        temp_socket = temp_context.socket(zmq.SUB)
        temp_socket.connect ("tcp://127.0.0.1:5678")
        temp_socket.setsockopt(zmq.SUBSCRIBE, "SimulatedLaserPower")

        pub_wrap = ZMQWrapper.Publisher("SimulatedLaserPower", 1)
        result = temp_socket.recv()
        topic, message_data = result.split(",")
        assert topic == "SimulatedLaserPower"
        assert message_data != -1.0
