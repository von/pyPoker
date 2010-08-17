#!/usr/bin/env python
"""Unittests for PokerGame module"""

from pyPoker.Hand import Board, FiveCardStudHand
from pyPoker import HoldEm
from pyPoker.PokerGame import FiveCardStudHiLoGame
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testFiveCardStudHiLoGame(self):
	"""Test FiveCardStudHiLoGame."""
	game = FiveCardStudHiLoGame()
	game.addHand(FiveCardStudHand.fromString("AS 2S"))
	game.addHand(FiveCardStudHand.fromString("KH KD"))
	game.simulateGames(numGames=10)

if __name__ == "__main__":
    unittest.main()
