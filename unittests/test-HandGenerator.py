#!/usr/bin/env python
"""Unittests for HandGenerator module"""

from pyPoker.HandGenerator import HandGenerationException
from pyPoker import HoldEm
from pyPoker.Deck import Deck
from pyPoker.Cards import Card, Rank, Suit
from pyPoker.slanskyHands import SlanskyHand
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testHoldEmHandGeneration(self):
	hg = HoldEm.HandGenerator()
	hg.addHands([HoldEm.Hand([Card((Rank.JACK, Suit.CLUBS)),
                                  Card((Rank.TEN, Suit.CLUBS))])])
	hand = hg.generateHand()
	self.assertEquals(hand[0].rank, Rank.JACK)
	self.assertEquals(hand[0].suit, Suit.CLUBS)
	self.assertEquals(hand[1].rank, Rank.TEN)
	self.assertEquals(hand[0].suit, Suit.CLUBS)

    def testGeneratingSameHandTwice(self):
	hg = HoldEm.HandGenerator()
	hg.addHands([HoldEm.Hand([Card((Rank.JACK, Suit.CLUBS)),
                                  Card((Rank.TEN, Suit.CLUBS))])])
	deck = Deck()
	hand = hg.generateHand(deck=deck)
	# Should fail trying to draw same two cards from deck again
	self.assertRaises(HandGenerationException, hg.generateHand, deck)

    def testMultipleGeneration(self):
	hg = HoldEm.HandGenerator()
	hg.addHands(SlanskyHand['class1'])
	for handNum in range(100):
	    hand = hg.generateHand()
	    if not SlanskyHand['class1'].containsHand(hand):
		self.fail("Generated hand (%s) not valid." % hand)

if __name__ == "__main__":
    unittest.main()
