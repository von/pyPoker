#!/usr/bin/env python
"""Unittests for PokerGame module"""

from pyPoker.Hand import Board, HoldEmHand, FiveCardStudHand, OmahaHand
from pyPoker.PokerGame import HoldEmGame, FiveCardStudHiLoGame, OmahaGame, OmahaHiLoGame
from pyPoker.HandGenerator import HoldEmHandGenerator
from pyPoker.slanskyHands import SlanskyHand
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testHoldEmGame(self):
	"""Test HoleEmGame."""
	game = HoldEmGame()
	game.setBoard(Board.fromString("5C 2S 4D"))
	game.addHand(HoldEmHand.fromString("AC 2C"))
	game.addHand(HoldEmHand.fromString("AH KH"))
	game.simulateGames(numGames=10)

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

    def testHandGenerator(self):
	"""Test HoleEmGame with HandGenerator."""
	game = HoldEmGame()
	game.addHand(HoldEmHand.fromString("AC 2C"))
	game.addHand(HoldEmHand.fromString("AH KH"))
	game.addHandGenerator(HoldEmHandGenerator(SlanskyHand['class1']))
	game.addHandGenerator(HoldEmHandGenerator(SlanskyHand['class2']))
	game.addHandGenerator(HoldEmHandGenerator(SlanskyHand['class3']))
	game.addHandGenerator(HoldEmHandGenerator(SlanskyHand['class4']))
	game.simulateGames(numGames=10)

if __name__ == "__main__":
    unittest.main()
