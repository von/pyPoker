#!/usr/bin/env python
"""Unittests for Hand module"""

from pyPoker.Cards import Card, Suit, Rank
from pyPoker.Hand import Hand, Board, TooManyCardsException
from pyPoker import HoldEm

import testing

class TestSequenceFunctions(testing.TestCase):

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

    def test_too_many_cards(self):
        """Test adding too many cards to a hand."""
        hand = Hand.fromString("AC 2C 3C 4C 5C")
        self.assertEquals(len(hand), 5)
        with self.assertRaises(TooManyCardsException):
            hand.append(Card.fromString("6C"))
        self.assertEquals(len(hand), 5)

    def testCombinations(self):
	"""Test basic hand combinatins."""
	hand = Hand.fromString("8C 9D 7C 6S AH")
        self.assert_iterator(hand.combinations(2),
                             count=10,
                             assert_item_function=lambda i: len(i)==2)

    def testBoardCombinations(self):
	"""Test combinations with board."""
	hand = HoldEm.Hand.fromString("AD 2D")
	board = Board.fromString("3D 4D 5D")
	hand.setBoard(board)
        self.assert_iterator(hand.combinations(2),
                             count=10,
                             assert_item_function=lambda i: len(i) == 2)
        self.assert_iterator(hand.combinations(5),
                             count=1,
                             assert_item_function=lambda i: len(i) == 5)
	board.addCardFromString("6D")
        self.assert_iterator(hand.combinations(5),
                             count=6,
                             assert_item_function=lambda i: len(i) == 5)
	board.addCardFromString("7D")
        self.assert_iterator(hand.combinations(5),
                             count=21,
                             assert_item_function=lambda i: len(i) == 5)

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

if __name__ == "__main__":
    testing.main()
