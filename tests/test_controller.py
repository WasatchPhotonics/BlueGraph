""" unit and functional tests for bluegraph application.
"""
        
from bluegraph import control
from bluegraph.devices import Simulation

class TestController:
    def test_control_creates_simulation_device(self, qtbot):
        simulator = control.BlueGraphController()

        # From the documentation examples - do you need to register the
        # widgets?
        #window = Window()
        #window.show()
        #qtbot.addWidget(window)

        assert isinstance(simulator.device,
                          Simulation.SimulatedLaserPowerMeter)

    def test_control_creates_bluegraph_widget(self, qtbot):
        simulator = control.BlueGraphController()
        with qtbot.wait_signal(simulator.form.customContextMenuRequested, timeout=2000):
            simulator.form.show()
        assert simulator.form.width() == 805
        assert simulator.form.height() == 355

    def test_control_fps_is_available(self, qtbot):
        simulator = control.BlueGraphController()
       
        # Don't wait for just 1 second, as pyqtgraph loading takes
        # consumes that time.
        with qtbot.wait_signal(simulator.form.customContextMenuRequested, timeout=2000):
            simulator.form.show()
    
        assert simulator.fps.rate() > 1000
