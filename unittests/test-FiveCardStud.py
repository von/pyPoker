#!/usr/bin/env python
"""Unittests for Five Card Stude module"""

import testing

from pyPoker import FiveCardStud
from pyPoker.PokerGame import Result, Stats

class TestSequenceFunctions(testing.TestCase):

    def setUp(self):
	pass

    def test_Simulator(self):
        """Test FiveCardStud.Simulator"""
        simulator = FiveCardStud.Simulator()
        self.assertIsNotNone(simulator)
        self.assertEqual(simulator.GAME_NAME, "Five-card Stud")
        result = simulator.simulate_game()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        stats = simulator.simulate_games(number_of_games=4)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, Stats)

    def test_HiLoSimulator(self):
        """Test FiveCardStud.HiLoSimulator"""
        simulator = FiveCardStud.HiLoSimulator()
        self.assertIsNotNone(simulator)
        self.assertEqual(simulator.GAME_NAME, "Five-card Stud Hi/Lo")
        result = simulator.simulate_game()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        stats = simulator.simulate_games(number_of_games=4)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, Stats)

if __name__ == "__main__":
    testing.main()
