#!/usr/bin/env python
"""Unittests for Five Card Stude module"""

from pyPoker import FiveCardStud
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testFiveCardStudHiLoGame(self):
	"""Test FiveCardStudHiLoGame."""
	game = FiveCardStud.HiLoGame()
	game.addHand(FiveCardStud.Hand.fromString("AS 2S"))
	game.addHand(FiveCardStud.Hand.fromString("KH KD"))
	game.simulateGames(numGames=10)

if __name__ == "__main__":
    unittest.main()
