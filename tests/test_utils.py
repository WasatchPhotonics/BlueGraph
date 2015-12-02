""" Utils tests for BlueGraph application
"""

from PySide import QtCore, QtTest

from bluegraph import utils

class TestFPS:

    def test_fps_creation(self, qtbot):
        # Create the object
        fps = utils.SimpleFPS()

        # Verify current rate is -1
        assert fps.rate() == -1

        # Let the app run for one second with no ticks, verify it's
        # still 0
        simulator = utils.Basic()
        known_signal = simulator.customContextMenuRequested
        with qtbot.wait_signal(known_signal, timeout=200):
            simulator.show()
        assert fps.rate() == 0

    def test_fps_updates(self, qtbot):
        # Create the object
        fps = utils.SimpleFPS()

        # Send it some ticks
        for i in range(10):
            fps.tick()

        # verify they match the expected count after a delay
        simulator = utils.Basic()
        known_signal = simulator.customContextMenuRequested
        with qtbot.wait_signal(known_signal, timeout=200):
            simulator.show()

        assert fps.rate() == 10

        # Wait another second, verify that the rate drops to zero
        with qtbot.wait_signal(known_signal, timeout=1000):
            simulator.show()
        assert fps.rate() == 0

