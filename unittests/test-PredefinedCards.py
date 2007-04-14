#!/usr/bin/env python
######################################################################
#
# Unittests for PredefinedCards module
#
# $Id$
######################################################################

from pyPoker.PredefinedCards import *
import unittest


class TestSequenceFunctions(unittest.TestCase):
    def testSuits(self):
	"""Test suites."""
	suit1 = Clubs
	suit2 = Spades
	suit3 = Hearts
	suit4 = Diamonds

    def testRanks(self):
	"""Test ranks."""
	r = Ace
	r = Two
	r = Three
	r = Four
	r = Five
	r = Six
	r = Seven
	r = Eight
	r = Nine
	r = Ten
	r = Jack
	r = Queen
	r = King

    def testCards(self):
	"""Test cards."""
	c = TwoOfClubs
	c = SevenOfDiamonds
	c = QueenOfHearts
	c = AceOfSpades
	c = JackOfClubs

if __name__ == "__main__":
    unittest.main()
