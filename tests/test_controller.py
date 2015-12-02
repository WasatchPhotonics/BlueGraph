""" unit and functional tests for bluegraph application.
"""

from PySide import QtTest

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
        known_signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(known_signal, timeout=2000):
            simulator.form.show()
        assert simulator.form.width() > 5
        assert simulator.form.height() > 5
        #assert simulator.form.width() == 805
        #assert simulator.form.height() == 355

    def test_control_fps_is_available(self, qtbot):
        simulator = control.BlueGraphController()

        # Don't wait for just 1 second, as pyqtgraph loading takes
        # consumes that time.
        known_signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(known_signal, timeout=2000):
            simulator.form.show()

        assert simulator.fps.rate() > 10

   # def test_control_fps_signal_updates_interface(self, qtbot):

    def test_close_event_triggered(self, qtbot):
        simulator = control.BlueGraphController()
        QtTest.QTest.qWaitForWindowShown(simulator.form)
        known_signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(known_signal, timeout=2000):
            simulator.form.show()
        simulator.form.closeEvent(None)
