#!/usr/bin/env python
"""Unittests for LowRanker module"""

from pyPoker import Omaha
from pyPoker.Cards import Cards, Rank, Suit
from pyPoker.Hand import Board, Hand
from pyPoker.Hands import Hands
from pyPoker.LowRanker import LowRanker
from pyPoker.PokerRank import PokerRank
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.ranker = LowRanker()


    def testBasicLowRanking(self):
	"""Verify ranking for low hand."""
	rank = self.ranker.rankHand(Hand.fromString("AS 8C 7S 4D 3H"))
	self.assertEqual(rank.getType(), PokerRank.HIGH_CARD,
                         "%s != HIGH_CARD" % rank)
	self.assertEqual(rank.getPrimaryCardRank(), Rank.EIGHT,
			 "%s != 8, kickers = %s" % (rank.getPrimaryCardRank(),
						    rank.kickersAsString()))
	self.assertEqual(rank.isEightOrBetterLow(), True,
			 "\"%s\".isEightOrBetterLow() != True" % rank)
        kickers = rank.getKickerRanks()
        self.assertEqual(len(kickers), 4,
                         "len(kickers) = %d != 4" % len(kickers))
        self.assertEqual(kickers[0], Rank.SEVEN,
                         "kickers[0] == %s != SEVEN" % kickers[0])
        self.assertEqual(kickers[1], Rank.FOUR,
                         "kickers[1] == %s != FOUR" % kickers[1])
        self.assertEqual(kickers[2], Rank.THREE,
                         "kickers[2] == %s != THREE" % kickers[2])
        self.assertEqual(kickers[3], Rank.ACE_LOW,
                         "kickers[3] == %s != ACE (low)" % kickers[3])

    def testLowRanking(self):
	"""Test basic low hand ranking."""
	hands = Hands()
	#
	# List in ascending order, so that if any hand compares greater than
	# a preceding hand, we know there is a problem
	hands.addHandsFromStrings([
		# Wheel
		"5S 4C 3D 2C AS",
		# Ten-high
		"TS 9C 8D 7C 6S",
		# Jack-high
		"AS JS TS 7S 3S",
		# High-card Jack
		"JC TS 9D 6H 2C",
		# High-card King
		"KC TS 9D 6H 2C",
		# King-high
		"KS JS TS 7S 3S",
		# King-high
		"AS KC QD JC TS",
		# King-high
		"KS QS JS TS 9S",
		# Pair of aces
		"AS AC 8D 3C 2S",
		# Pair of queens
		"QS QC 8D 3C 2S",
		# Aces and eights
		"AS AC 8D 8C 2S",
		# Queens and Jacks
		"QS QC JD JC 2S",
		# Queens and Jacks, higher kicker
		"QS QC JD JC 3S",
		# Trip Aces
		"AS AC AD 8C 2S",
		# Trip Fours
		"QS 9D 4S 4H 4D",
		# Trip Tens
		"JC TS TC TD 2S",
		# Aces full of sevens
		"AS AC AD 7C 7S",
		# Aces full of eights
		"AS AC AD 8C 8S",
		# Kings full of jacks
		"KS KC KD JC JS",
		# Quad aces
		"AS AC AD AH 8S",
		# Quad aces, higher kicker
		"AS AC AD AH TS",
		# Quad threes
		"9S 3S 3C 3D 3H"])


	ranks = [self.ranker.rankHand(hand) for hand in hands]
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


    def testBestHand(self):
        """Test bestHand() method"""
        hands = [
            Hand.fromString("AC 9D KS 3D KH"), # Pair of Kings
            Hand.fromString("9C TS QH JC 8H"), # Q-high
            Hand.fromString("KD TH 7C 6C 2H"), # K-high
            Hand.fromString("AD JD 8D 4D 2D"), # J-high
            Hand.fromString("7S QD QS QC 6D"), # Trip queens
            Hand.fromString("8S 7C 2C 3D 5H"), # 8-high
            ]
        best_hands, best_rank = self.ranker.bestHand(hands)
        self.assertIsNotNone(best_hands)
        self.assertIsInstance(best_hands, list)
        self.assertEqual(len(best_hands), 1)
        self.assertEqual(best_hands[0], 5) # 8-high
        self.assertIsNotNone(best_rank)
        self.assertIsInstance(best_rank, PokerRank)
        self.assertEqual(best_rank.getType(), PokerRank.HIGH_CARD)
        self.assertEqual(best_rank.getPrimaryCardRank(), Rank.EIGHT)

    def testOmahaLow(self):
	"""Test Omaha low hand ranking."""
	hand = Omaha.Hand.fromString("5D 6H 9H 3C")
	board = Board.fromString("4H 6C JH KH 8C")
	hand.setBoard(board)
	rank = self.ranker.rankHand(hand)
	self.assertEqual(rank.getType(), PokerRank.HIGH_CARD,
                         "rank = %s" % rank)
	self.assertEqual(rank.getPrimaryCardRank(), Rank.EIGHT,
			 "primaryCard = %s kickers = %s" % (rank.getPrimaryCardRank(),
							    rank.kickersAsString()))

    def testOmahaLow2(self):
	"""Test Omaha low hand ranking."""
	hand = Omaha.Hand.fromString("QC AH TC 8C")
	board = Board.fromString("2H JH 4D 6H 3H")
	hand.setBoard(board)
	rank = self.ranker.rankHand(hand)
	self.assertEqual(rank.getType(), PokerRank.HIGH_CARD,
                         "rank = %s" % rank)
	self.assertEqual(rank.getPrimaryCardRank(), Rank.EIGHT,
			 "primaryCard = %s kickers = %s" % (rank.getPrimaryCardRank(),
							    rank.kickersAsString()))


if __name__ == "__main__":
    unittest.main()

