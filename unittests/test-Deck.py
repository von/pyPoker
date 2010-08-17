#!/usr/bin/env python
"""Unittests for Deck module"""

from pyPoker.Hand import Hand
from pyPoker import HoldEm
from pyPoker.Deck import Deck
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testDesk(self):
	"""Test basic deck construction and shuffling."""
	deck = Deck()
        self.assertEqual(len(deck), 52, "Deck has %d cards!" % len(deck))
	deck.shuffle()
	deck.reset()

    def testDealHand(self):
	"""Test basic dealing to a single hand."""
	hand = Hand()
	deck = Deck()
	deck.shuffle()
	deck.deal(hand,5)
	self.assertEquals(len(hand), 5)

    def testDealHands(self):
	"""Test dealing to multiple hands."""
	hands = [Hand(), Hand(), Hand(), Hand()]
	deck = Deck()
	deck.shuffle()
	deck.deal(hands, 5)
	for hand in hands:
	    self.assertEquals(len(hand), 5)

    def testCreateHands(self):
	"""Test creating multiple hands."""
	deck = Deck()
	deck.shuffle()
	hands = deck.createHands(8, handClass=HoldEm.Hand)
	self.assertEquals(len(hands), 8)
	for hand in hands:
	    self.assertEquals(len(hand), 2)

if __name__ == "__main__":
    unittest.main()
