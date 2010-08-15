#!/usr/bin/env python
"""Unittests for Cards module"""

from pyPoker.Cards import Card, Cards, Suit, Rank, BadRankException
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def testSuitStr(self):
        """Test converting Suit to string."""
        s = Suit(Suit.CLUBS)
        self.assertEqual(str(s), "C")
        self.assertEqual(s.str(), "C")

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
	ace = Rank(Rank.ACE_LOW)
	for r in Rank.ranks:
	    rank = Rank(r)
	    if ace != rank:
		self.assert_(ace < rank, "!low ace < %s" % rank)

    def testBadLowRank(self):
	try:
	    r = Rank(Rank.ACE_LOW - 1)
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

    def testAceLowHigh(self):
        """Test making Aces high and low."""
        c = Card.fromString("AC")
        self.assertEquals(c.rank, Rank.ACE)
        c.makeAcesLow()
        self.assertEquals(c.rank, Rank.ACE_LOW)
        c.makeAcesHigh()
        self.assertEquals(c.rank, Rank.ACE)

    def testAceLowHighNonAce(self):
        """Test making sure makeAcesLow() and makeAcesHigh() have no effect on non-ace"""
        c = Card.fromString("9D")
        self.assertEquals(c.rank, Rank.NINE)
        c.makeAcesLow()
        self.assertEquals(c.rank, Rank.NINE)
        c.makeAcesHigh()
        self.assertEquals(c.rank, Rank.NINE)

    def testSort(self):
	cards = Cards().fromString("3S KH 7H JD TS")
	cards.sort()
	self.assertEquals(cards[0], Rank.THREE, "%s" % cards)
	self.assertEquals(cards[1], Rank.SEVEN, "%s" % cards)
	self.assertEquals(cards[2], Rank.TEN, "%s" % cards)
	self.assertEquals(cards[3], Rank.JACK, "%s" % cards)
	self.assertEquals(cards[4], Rank.KING, "%s" % cards)
	cards.sort(reverse=True)
	self.assertEquals(cards[0], Rank.KING, "%s" % cards)
	self.assertEquals(cards[1], Rank.JACK, "%s" % cards)
	self.assertEquals(cards[2], Rank.TEN, "%s" % cards)
	self.assertEquals(cards[3], Rank.SEVEN, "%s" % cards)
	self.assertEquals(cards[4], Rank.THREE, "%s" % cards)
	
    def testAceHighLowSort(self):
        cards = Cards().fromString("7D AH KS 2C 9D")
        cards.sort(reverse=True)
        self.assertEquals(cards[0], Rank.ACE, "%s" % cards)
	self.assertEquals(cards[1], Rank.KING, "%s" % cards)
	self.assertEquals(cards[2], Rank.NINE, "%s" % cards)
	self.assertEquals(cards[3], Rank.SEVEN, "%s" % cards)
	self.assertEquals(cards[4], Rank.TWO, "%s" % cards)
        cards.makeAcesLow()
        cards.sort(reverse=True)
	self.assertEquals(cards[0], Rank.KING, "%s" % cards)
	self.assertEquals(cards[1], Rank.NINE, "%s" % cards)
	self.assertEquals(cards[2], Rank.SEVEN, "%s" % cards)
	self.assertEquals(cards[3], Rank.TWO, "%s" % cards)
        self.assertEquals(cards[4], Rank.ACE_LOW, "%s" % cards)

    def testCombinations(self):
	"""Test basic hand combinatins."""
	cards = Cards.fromString("8C 9D 7C 6S AH")
	count = 0
	for combs in cards.combinations(2):
	    count += 1
	    self.assertEquals(len(combs), 2)
	self.assertEquals(count, 10)
	count = 0
	for combs in cards.combinations(5):
	    count += 1
	    self.assertEquals(len(combs), 5)
	self.assertEquals(count, 1)
	cards.addCardsFromString("AS 2C")
	count = 0
	for combs in cards.combinations(5):
	    count += 1
	    self.assertEquals(len(combs), 5)
	self.assertEquals(count, 21)

if __name__ == "__main__":
    unittest.main()
