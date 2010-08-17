#!/usr/bin/env python
"""Unittests for PokerGame module"""

from pyPoker.Hand import Board, FiveCardStudHand, OmahaHand
from pyPoker import HoldEm
from pyPoker.PokerGame import FiveCardStudHiLoGame, OmahaGame, OmahaHiLoGame
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

    def testOmahaGame(self):
	"""Test OmahaGame."""
	game = OmahaGame()
	game.setBoard(Board.fromString("5C 2S 4D"))
	game.addHand(OmahaHand.fromString("AC 2C"))
	game.addHand(OmahaHand.fromString("AH KH"))
	game.simulateGames(numGames=10)

    def testOmahaHiLoGame(self):
	"""Test OmahaHiLoGame."""
	game = OmahaHiLoGame()
	game.setBoard(Board.fromString("5C 2S 4D"))
	game.addHand(OmahaHand.fromString("AC 2C"))
	game.addHand(OmahaHand.fromString("AH KH"))
	game.simulateGames(numGames=10)

if __name__ == "__main__":
    unittest.main()
