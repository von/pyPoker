#!/usr/bin/env python
######################################################################
#
# Unittests for Cards module
#
# $Id$
######################################################################

from pyPoker.Cards import Card, Cards, Suit, Rank, BadRankException
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	Rank.acesAreHigh()

    def testRankCompare(self):
	"""Test basic rank comparisons."""
	for r in Rank.ranks:
	    r1 = Rank(r)
	    try:
		r2 = Rank(r+1)
	    except BadRankException:
		break
	    self.assert_(r1 < r2, "!%s < %s" % (r1, r2))

    def testRankCompareAcesLow(self):
	Rank.acesAreLow()
	ace = Rank(Rank.ACE)
	for r in Rank.ranks:
	    rank = Rank(r)
	    if ace != rank:
		self.assert_(ace < rank, "!low ace < %s" % rank)

    def testBadLowRank(self):
	try:
	    r = Rank(Rank.TWO - 1)
	except BadRankException:
	    pass
	else:
	    self.fail("Rank(Rank.TWO - 1) failed to raise exception")
	    
    def testBadHighRank(self):
	try:
	    r = Rank(Rank.ACE + 1)
	except BadRankException:
	    pass
	else:
	    self.fail("Rank(Rank.ACE + 1) failed to raise exception")

    def testBasicConstruction(self):
	c = Card().fromString("8C")
	self.assertEquals(c.rank, Rank.EIGHT)
	self.assertEquals(c.suit, Suit.CLUBS)

    def testSort(self):
	cards = Cards().fromString("3S KH 7H JD TS")
	cards.sort()
	self.assertEquals(cards[0], Rank.KING, "%s" % cards)
	self.assertEquals(cards[1], Rank.JACK, "%s" % cards)
	self.assertEquals(cards[2], Rank.TEN, "%s" % cards)
	self.assertEquals(cards[3], Rank.SEVEN, "%s" % cards)
	self.assertEquals(cards[4], Rank.THREE, "%s" % cards)

if __name__ == "__main__":
    unittest.main()
