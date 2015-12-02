""" unit and functional tests for bluegraph application.
"""

from PySide import QtTest

from bluegraph import control
from bluegraph.devices import Simulation

class TestController:
    def test_control_creates_simulation_device(self, qtbot):
        simulator = control.BlueGraphController("SimulatedLaser")
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

    def test_close_event_triggered(self, qtbot):
        simulator = control.BlueGraphController()
        QtTest.QTest.qWaitForWindowShown(simulator.form)
        known_signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(known_signal, timeout=2000):
            simulator.form.show()
        simulator.form.closeEvent(None)

    def test_control_creates_specified_device(self, qtbot):
        simulator = control.BlueGraphController()
        assert isinstance(simulator.device, control.InternalSlow)

        simulator = control.BlueGraphController("SimulatedSpectra")
        assert isinstance(simulator.device,
                          Simulation.SimulatedSpectra)

    def test_simulated_internal_random_display_speed(self, qtbot):
        simulator = control.BlueGraphController("InternalSlow")
        known_signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(known_signal, timeout=2000):
            simulator.form.show()

        assert simulator.fps.rate() >= 9
        assert simulator.fps.rate() <= 11

    def test_simulated_spectra_displays_fast(self, qtbot):
        simulator = control.BlueGraphController("SimulatedSpectra")
        known_signal = simulator.form.customContextMenuRequested
        with qtbot.wait_signal(known_signal, timeout=2000):
            simulator.form.show()

        assert simulator.fps.rate() >= 20
        assert simulator.fps.rate() <= 200
        print "Actual measured rate: %s" % simulator.fps.rate()
