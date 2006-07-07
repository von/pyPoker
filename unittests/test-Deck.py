#!/usr/bin/env python
######################################################################
#
# Unittests for Deck module
#
# $Id$
######################################################################

from pyPoker.Hand import Hand
from pyPoker.Deck import Deck
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testDesk(self):
	"""Test basic deck construction and shuffling."""
	deck = Deck()
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

if __name__ == "__main__":
    unittest.main()
