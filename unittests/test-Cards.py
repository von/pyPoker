#!/usr/bin/env python
"""Unittests for Cards module"""

from pyPoker.Cards import Card, Cards, Suit, Rank, BadRankException

import testing

class TestSequenceFunctions(testing.TestCase):

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
	    self.assertLess(r1, r2, "!%s < %s" % (r1, r2))

    def testRankCompareAcesLow(self):
	ace = Rank(Rank.ACE_LOW)
	for r in Rank.ranks:
	    rank = Rank(r)
	    if ace != rank:
		self.assertLess(ace, rank, "!low ace < %s" % rank)

    def testBadLowRank(self):
	try:
	    r = Rank(Rank.ACE_LOW - 1)
	except BadRankException:
	    pass
	else:
	    self.fail("Rank(Rank.TWO - 1) failed to raise exception")
	    
    def testBadHighRank(self):
        with self.assertRaises(BadRankException):
	    r = Rank(Rank.ACE + 1)

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

    def testIsEightOrLower(self):
        """Test IsEightOrLower() method"""
        for rank in range(Rank.ACE_LOW, Rank.NINE):
            c = Card((rank, Suit.CLUBS))
            self.assertTrue(c.isEightOrLower(), "%s failed" % c)
        for rank in range(Rank.NINE, Rank.ACE):
            c = Card((rank, Suit.HEARTS))
            self.assertFalse(c.isEightOrLower(), "%s failed" % c)
        c = Card((Rank.ACE, Suit.DIAMONDS))
        self.assertTrue(c.isEightOrLower(), "%s failed" % c)
            
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
        self.assert_iterator(cards.combinations(2),
                             count=10,
                             assert_item_function=lambda i: len(i)==2)
        self.assert_iterator(cards.combinations(5),
                             count=1,
                             assert_item_function=lambda i: len(i)==5)
	cards.addCardsFromString("AS 2C")
        self.assert_iterator(cards.combinations(5),
                             count=21,
                             assert_item_function=lambda i: len(i)==5)

    def testGetEightOrLower(self):
        """Test getEightOrLower() method"""
        cards = Cards.fromString("AC TH 7D 8S QD")
        low_cards = cards.getEightOrLower()
        self.assertIsNotNone(low_cards)
        self.assertEqual(len(low_cards), 3)
        self.assertListEqual(low_cards, Cards.fromString("AC 7D 8S"))
        cards = Cards.fromString("AC 5H 7D 8S 2D")
        low_cards = cards.getEightOrLower()
        self.assertIsNotNone(low_cards)
        self.assertEqual(len(low_cards), 5)
        self.assertListEqual(low_cards, Cards.fromString("AC 5H 7D 8S 2D"))
        cards = Cards.fromString("JC TH 9D KS QD")
        low_cards = cards.getEightOrLower()
        self.assertIsNotNone(low_cards)
        self.assertEqual(len(low_cards), 0)

    def testRemoveDuplicateRranks(self):
        """Test removeDuplicateRanks() method"""
        # Two 4's and one ace should be removed
        cards = Cards.fromString("8D 4C AH 9D 4H KC 4S AC")
        pruned_cards = cards.removeDuplicateRanks()
        self.assertIsNotNone(pruned_cards)
        self.assertEqual(len(pruned_cards), 5)
        # Nothing should be removed
        cards = Cards.fromString("8D 4C AH 9D 5H KC 3S JC")
        pruned_cards = cards.removeDuplicateRanks()
        self.assertIsNotNone(pruned_cards)
        self.assertEqual(len(pruned_cards), 8)

if __name__ == "__main__":
    testing.main()
