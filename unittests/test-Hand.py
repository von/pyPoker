#!/usr/bin/env python
"""Unittests for Hand module"""

from pyPoker.Cards import Card, Suit, Rank
from pyPoker.Hand import Hand, Board, OmahaHand, HoldEmHand
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testHandConstruction(self):
	"""Test basic hand construction"""
	hand = Hand.fromString("8C")
	self.assertEquals(hand[0].suit, Suit.CLUBS)
	self.assertEquals(hand[0].rank, Rank.EIGHT)
	hand.addCardsFromString("9D TH")
	self.assertEquals(hand[1].suit, Suit.DIAMONDS)
	self.assertEquals(hand[1].rank, Rank.NINE)
	self.assertEquals(hand[2].suit, Suit.HEARTS)
	self.assertEquals(hand[2].rank, Rank.TEN)

    def testCombinations(self):
	"""Test basic hand combinatins."""
	hand = Hand.fromString("8C 9D 7C 6S AH")
	count = 0
	for combs in hand.combinations(2):
	    count += 1
	    self.assertEquals(len(combs), 2)
	self.assertEquals(count, 10)

    def testBoardCombinations(self):
	"""Test combinations with board."""
	hand = HoldEmHand.fromString("AD 2D")
	board = Board.fromString("3D 4D 5D")
	hand.setBoard(board)
	count = 0
	for combs in hand.combinations(2):
	    count += 1
	    self.assertEquals(len(combs), 2)
	self.assertEquals(count, 10)
	count = 0
	for combs in hand.combinations(5):
	    count += 1
	    self.assertEquals(len(combs), 5)
	self.assertEquals(count, 1)
	board.addCardFromString("6D")
	count = 0
	for combs in hand.combinations(5):
	    count += 1
	    self.assertEquals(len(combs), 5)
	self.assertEquals(count, 6)
	board.addCardFromString("7D")
	count = 0
	for combs in hand.combinations(5):
	    count += 1
	    self.assertEquals(len(combs), 5)
	self.assertEquals(count, 21)

    def testBoardToString(self):
	board = Board.fromString("7C 8C 9C")
	self.assertEqual("%s" % board, "7C 8C 9C xx xx")

    def testBoardEightLow(self):
	for board in [ "AC 2C 3C 4C 5C",
		       "AC AH 3C 4C 9C",
		       "AC 2C 8C TC KC" ]:
	    self.assertEqual(Board.fromString(board).eightLowPossible(),
			     True, "%s not True" % board)
	for board in [ "AC AH 8C 9D TH",
		       "AC AH 2D TC JH",
		       "8C 9H TD JC QH",
		       "AC 2C 9C TC JD" ]:
	    self.assertEqual(Board.fromString(board).eightLowPossible(),
			     False, "%s not False" % board)

    def testOmahaLowPossible(self):
	for hand in [ "AC 2C 3C 4D",
		      "AC AD 2C 2D",
		      "7C 8C 9C TC",
		      "AC 8C JC KC" ]:
	    self.assertEqual(OmahaHand.fromString(hand).eightLowPossible(),
			     True, "%s not True" % hand)
	for hand in [ "AC AH AS 9D",
		      "AC AD 9C TD",
		      "7C 9C TC KC",
		      "AC 9C JC KC" ]:
	    self.assertEqual(OmahaHand.fromString(hand).eightLowPossible(),
			     False, "%s not False" % hand)

    def testOmahaCombinations(self):
	"""Testing Omaha combinations."""
	hand = OmahaHand.fromString("AC 2C 3C 4C");
	board = Board.fromString("5C 6C 7C 8C 9C");
	hand.setBoard(board)
	count = 0
	for combs in hand.combinations(2):
	    count += 1
	    self.assertEquals(len(combs), 2, "combs = %s" % combs)
	self.assertEquals(count, 6)
	count = 0
	for combs in hand.hands():
	    count += 1
	    self.assertEquals(len(combs), 5, "combs = %s" % combs)
	self.assertEquals(count, 60)

    def testOmahaPoints(self):
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
	    value = OmahaHand.fromString(hand).pointValue()
	    self.assertEquals(value, hands[hand],
			      "%s == %d != %d points" % (hand, value, 
							 hands[hand]))
			  

if __name__ == "__main__":
    unittest.main()
