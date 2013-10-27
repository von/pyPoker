#!/usr/bin/env python
"""Unittests for Seven Card Stud module"""

import testing

from pyPoker import SevenCardStud
from pyPoker.PokerGame import Result, Stats, TooManyHandsException

class TestSequenceFunctions(testing.TestCase):

    def setUp(self):
	pass

    def test_Simulator(self):
        """Test SevenCardStud.Simulator"""
        simulator = SevenCardStud.Simulator()
        self.assertIsNotNone(simulator)
        self.assertEqual(simulator.GAME_NAME, "Seven-card Stud")
        result = simulator.simulate_game()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        stats = simulator.simulate_games(number_of_games=4)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, Stats)

    def test_HiLoSimulator(self):
        """Test SevenCardStud.HiLoSimulator"""
        simulator = SevenCardStud.HiLoSimulator()
        self.assertIsNotNone(simulator)
        self.assertEqual(simulator.GAME_NAME, "Seven-card Stud Hi/Lo")
        result = simulator.simulate_game()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        stats = simulator.simulate_games(number_of_games=4)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, Stats)

    def test_Simulator_TooManyHandsException(self):
        """Test SevenCardStud.Simulator generating NotEnoughCardsException"""
        self.assertRaises(TooManyHandsException,
                          SevenCardStud.Simulator,
                          number_of_hands=9)

if __name__ == "__main__":
    testing.main()
