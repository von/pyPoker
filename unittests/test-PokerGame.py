#!/usr/bin/env python
######################################################################
#
# Unittests for PokerGame module
#
# $Id$
#
######################################################################

from pyPoker.Hand import Board, HoldEmHand
from pyPoker.PokerGame import HoldEmGame
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

if __name__ == "__main__":
    unittest.main()
