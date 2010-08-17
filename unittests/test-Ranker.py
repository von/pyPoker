#!/usr/bin/env python
"""Unittests for Ranker module"""

from pyPoker.BitField import BitField
from pyPoker.Cards import Cards, Rank, Suit
from pyPoker.Hand import Board, Hand
from pyPoker.Hands import Hands
from pyPoker import HoldEm
from pyPoker import Omaha
from pyPoker.PokerRank import PokerRank
from pyPoker.Ranker import Ranker
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.ranker = Ranker()

    def testHandToBitField(self):
        """Test _handToBitField() method."""
        cards = Cards.fromString("JC 8D 4S KH 9D 3C")
        bitfield = self.ranker._handToBitField(cards)
        expectedBitfield = BitField()
        expectedBitfield += Rank.JACK
        expectedBitfield += Rank.EIGHT
        expectedBitfield += Rank.FOUR
        expectedBitfield += Rank.KING
        expectedBitfield += Rank.NINE
        expectedBitfield += Rank.THREE
        self.assertEqual(bitfield, expectedBitfield,
                         "%s != %s" % (bitfield, expectedBitfield))

    def testHandToSuitedBitFields(self):
        """Test _handToSuitedBitFields() method."""
        cards = Cards.fromString("QH 7C 4S KH 6D 7S AC")
        bitfield = self.ranker._handToBitField(cards)
        bitfields = self.ranker._handToSuitedBitFields(cards)
        expectedClubs = BitField()
        expectedClubs += Rank.SEVEN
        expectedClubs += Rank.ACE
        self.assertEqual(bitfields[Suit.CLUBS], expectedClubs,
                         "Clubs: %s != %s" % (bitfields[Suit.CLUBS],
                                              expectedClubs))
        expectedDiamonds = BitField()
        expectedDiamonds += Rank.SIX
        self.assertEqual(bitfields[Suit.DIAMONDS], expectedDiamonds,
                         "DIAMONDS: %s != %s" % (bitfields[Suit.DIAMONDS],
                                                 expectedDiamonds))
        expectedHearts = BitField()
        expectedHearts += Rank.QUEEN
        expectedHearts += Rank.KING
        self.assertEqual(bitfields[Suit.HEARTS], expectedHearts,
                         "HEARTS: %s != %s" % (bitfields[Suit.HEARTS],
                                               expectedHearts))
        expectedSpades = BitField()
        expectedSpades += Rank.FOUR
        expectedSpades += Rank.SEVEN
        self.assertEqual(bitfields[Suit.SPADES], expectedSpades,
                         "SPADES: %s != %s" % (bitfields[Suit.SPADES],
                                               expectedSpades))

    def testSuitedBitfieldToRankBitFields(self):
        """Test _suitedBitfieldsToRankBitfields() method."""
        cards = Cards.fromString("QH QC QS QD TC TH TD 2S 2C 2D 8H 8S 4H 4D 3S AH KS")
        bitfields = self.ranker._handToSuitedBitFields(cards)
        (singletonsBitField, pairsBitField, tripsBitField, quadsBitField) = self.ranker._suitedBitFieldsToRankedBitFields(bitfields)
        self.assertTrue(quadsBitField.testBit(Rank.QUEEN))
        self.assertTrue(tripsBitField.testBit(Rank.TEN))
        self.assertTrue(tripsBitField.testBit(Rank.TWO))
        self.assertTrue(pairsBitField.testBit(Rank.EIGHT))
        self.assertTrue(pairsBitField.testBit(Rank.FOUR))
        self.assertTrue(singletonsBitField.testBit(Rank.THREE))
        self.assertTrue(singletonsBitField.testBit(Rank.ACE))
        self.assertTrue(singletonsBitField.testBit(Rank.KING))
        # Check an arbitrary group of bits that shouldn't be set
        self.assertFalse(quadsBitField.testBit(Rank.JACK))
        self.assertFalse(tripsBitField.testBit(Rank.KING))
        self.assertFalse(tripsBitField.testBit(Rank.QUEEN))
        self.assertFalse(pairsBitField.testBit(Rank.SEVEN))
        self.assertFalse(pairsBitField.testBit(Rank.ACE))
        self.assertFalse(singletonsBitField.testBit(Rank.QUEEN))
        self.assertFalse(singletonsBitField.testBit(Rank.SIX))
        self.assertFalse(singletonsBitField.testBit(Rank.FOUR))

    def testHasStraight(self):
        """Test hasStriaght() method."""
        tests = [
            # cards as string, expected rank
            ("KC JS AC QS TH", Rank.ACE),
            ("KC JS 8C QS TH", None),
            ("KC JS AC QS TH 9S", Rank.ACE),
            ("KC JS QS TH 9S", Rank.KING),
            ("4S 3D AC 2S 5H", Rank.FIVE),
            ("8S 6D 5H 7S 4H", Rank.EIGHT),
            ("2D KH AC QD JH", None)
            ]
        for cards, rank in tests:
            bitfield = self.ranker._handToBitField(Cards.fromString(cards))
            self.assertEqual(self.ranker._hasStraight(bitfield), rank)

    def testRankHand(self):
        """Test rankHand() mathod."""
        rank = self.ranker.rankHand(Hand.fromString("JC TS 9D 6H 2C"))
        self.assertIsNotNone(rank)
        self.assertIsInstance(rank, PokerRank, type(rank))
        self.assertNotEqual(rank, 0)
        rankType = rank.getType()
        self.assertEqual(rankType, PokerRank.HIGH_CARD,
                         "rank = (%s) %d != HIGH_CARD" % (str(rankType), rankType))

    def testRanking(self):
	"""Test hand ranking."""
	hands = Hands()
	#
	# List in ascending order, so that if any hand compares greater than
	# a preceding hand, we know there is a problem
	hands.addHandsFromStrings([
		# High-card Jack
		"JC TS 9D 6H 2C",
		# High-card King
		"KC TS 9D 6H 2C",
		# Pair of queens
		"QS QC 8D 3C 2S",
		# Pair of aces
		"AS AC 8D 3C 2S",
		# Queens and Jacks
		"QS QC JD JC 2S",
		# Queens and Jacks, better kicker
		"QS QC JD JC 3S",
		# Aces and eights
		"AS AC 8D 8C 2S",
		# Trip Fours
		"QS 9D 4S 4H 4D",
                # Trip Fours, higher kicker
		"QS TD 4S 4H 4D",
		# Trip Tens
		"JC TS TC TD 2S",
		# Trip Aces
		"AS AC AD 8C 2S",
		# Wheel
		"5S 4C 3D 2C AS",
		# Straight, ten-high
		"TS 9C 8D 7C 6S",
		# Straight, ace-high
		"AS KC QD JC TS",
		# Flush, king-high
		"KS JS TS 7S 3S",
		# Flush, ace-high
		"AS JS TS 7S 3S",
		# Kings full of jacks
		"KS KC KD JC JS",
		# Aces full of sevens
		"AS AC AD 7C 7S",
		# Aces full of eights
		"AS AC AD 8C 8S",
		# Quad threes
		"9S 3S 3C 3D 3H",
		# Quad aces
		"AS AC AD AH 8S",
		# Quad aces, better kicker
		"AS AC AD AH TS",
		# Straight flush
		"KS QS JS TS 9S",
		# Royal flush
		"AS KS QS JS TS"])

	ranks = [self.ranker.rankHand(hand) for hand in hands]
        # Sanity check ranks
        for i, rank in enumerate(ranks):
            self.assertTrue(rank is not None,
                            "Hand \"%s\" rank == None" % hands[i])
            self.assertNotEqual(rank, 0,
                                "Hand \"%s\" rank == 0" % hands[i])
        # Make sure ranks are increasing
	for i in range(len(hands)):
	    for j in range(len(hands)):
		if (i < j):
		    self.assert_(ranks[i] < ranks[j],
				 "!(%d) %s (%s) < (%d) %s (%s)" %
				 ( i, hands[i], ranks[i],
				   j, hands[j], ranks[j]))
		elif (i > j):
		    self.assert_(ranks[i] > ranks[j],
				 "!(%d) %s (%s) > (%d) %s (%s)" %
				 ( i, hands[i], ranks[i],
				   j, hands[j], ranks[j]))
		else:
		    self.assertEqual(ranks[i], ranks[j],
				     "(%d) %s (%s) != (%d) %s (%s)" %
				     ( i, hands[i], ranks[i],
				       j, hands[j], ranks[j]))

    def testBoard(self):
	"""Verify ranking with board."""
	board = Board.fromString("5C 2S 4D")
	hand = HoldEm.Hand.fromString("AC 2C")
	hand.setBoard(board)
	rank = self.ranker.rankHand(hand)
	self.assertEqual(rank.getType(), PokerRank.PAIR,
                         "rankType = %d" % rank.getType())
	board.addCardFromString("AD")
	rank = self.ranker.rankHand(hand)
	self.assertEqual(rank.getType(), PokerRank.TWO_PAIR,
                         "rank = %d" % rank.getType())
	board.addCardFromString("3H")
	rank = self.ranker.rankHand(hand)
	self.assertEqual(rank.getType(), PokerRank.STRAIGHT,
                         "rank = %d" % rank.getType())

    def testOmaha(self):
	"""Test basic Omaha hand ranking."""
	hand = Omaha.Hand.fromString("7S QD 2D TD")
	board = Board.fromString("AS AD 4H TH 8D")
	hand.setBoard(board)
	rank = self.ranker.rankHand(hand)
	self.assertEqual(rank.getType(), PokerRank.TWO_PAIR, "rank = %s" % rank)
	self.assertEqual(rank.getPrimaryCardRank(), Rank.ACE,
			 "primaryCard = %s" % rank.getPrimaryCardRank())
	self.assertEqual(rank.getSecondaryCardRank(), Rank.TEN,
			 "secondaryCard = %s" % rank.getSecondaryCardRank())

if __name__ == "__main__":
    unittest.main()

