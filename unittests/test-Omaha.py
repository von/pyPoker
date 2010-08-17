#!/usr/bin/env python
"""Unittests for Omaha module"""

from pyPoker.Hand import Board
from pyPoker import Omaha
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def testLowPossible(self):
        """Test eightLowPossible() method"""
        # These hands have a possible low
	for hand in [ "AC 2C 3C 4D",
		      "AC AD 2C 2D",
		      "7C 8C 9C TC",
		      "AC 8C JC KC" ]:
	    self.assertEqual(Omaha.Hand.fromString(hand).eightLowPossible(),
			     True, "%s not True" % hand)
        # These hands don't have a possible low
	for hand in [ "AC AH AS 9D",
		      "AC AD 9C TD",
		      "7C 9C TC KC",
		      "AC 9C JC KC" ]:
	    self.assertEqual(Omaha.Hand.fromString(hand).eightLowPossible(),
			     False, "%s not False" % hand)

    def testCombinations(self):
	"""Testing Omaha combinations."""
	hand = Omaha.Hand.fromString("AC 2C 3C 4C");
	board = Board.fromString("5C 6C 7C 8C 9C");
	hand.setBoard(board)
	count = 0
	for combs in hand.combinations(2):
	    count += 1
	    self.assertEquals(len(combs), 2,
                              "combs = %s (len = %d)" % (combs, len(combs)))
	self.assertEquals(count, 6)
	count = 0
	for combs in hand.hands():
	    count += 1
	    self.assertEquals(len(combs), 5,
                              "combs = %s (len = %d)" % (combs, len(combs)))
	self.assertEquals(count, 60)

    def testPoints(self):
	"""Test Omaha HiLo point scoring."""
	hands = {
	    "AC AD 2C 3D":95,
	    "AC KH QD JS":16,
	    "AC AD KH KS":45,
	    "KS 2S QH 3H":22,
	    "AC AH AD 4H":35,
	    "AC 2C 3C 4H":74,
	    "7C 8C 9C TC":12
	    }
	for hand in hands.keys():
	    value = Omaha.Hand.fromString(hand).pointValue()
	    self.assertEquals(value, hands[hand],
			      "%s == %d != %d points" % (hand, value, 
							 hands[hand]))


    def testGame(self):
	"""Test OmahaGame."""
	game = Omaha.Game()
	game.setBoard(Board.fromString("5C 2S 4D"))
	game.addHand(Omaha.Hand.fromString("AC 2C"))
	game.addHand(Omaha.Hand.fromString("AH KH"))
	game.simulateGames(numGames=10)

    def testHiLoGame(self):
	"""Test OmahaHiLoGame."""
	game = Omaha.HiLoGame()
	game.setBoard(Board.fromString("5C 2S 4D"))
	game.addHand(Omaha.Hand.fromString("AC 2C"))
	game.addHand(Omaha.Hand.fromString("AH KH"))
	game.simulateGames(numGames=10)

if __name__ == "__main__":
    unittest.main()
