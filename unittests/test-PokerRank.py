#!/usr/bin/env python
######################################################################
#
# Unittests for PokerRank module
#
# $Id$
######################################################################

from pyPoker.Cards import Rank
from pyPoker.Hand import Hand, Hands, Board, OmahaHand, HoldEmHand
from pyPoker.PokerRank import PokerRank
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testBoard(self):
	"""Verify ranking with board."""
	board = Board.fromString("5C 2S 4D")
	hand = HoldEmHand.fromString("AC 2C")
	hand.setBoard(board)
	rank = PokerRank(hand)
	self.assertEqual(rank, PokerRank.PAIR, "rank = %s" % rank)
	board.addCardFromString("AD")
	rank = PokerRank(hand)
	self.assertEqual(rank, PokerRank.TWO_PAIR, "rank = %s" % rank)
	board.addCardFromString("3H")
	rank = PokerRank(hand)
	self.assertEqual(rank, PokerRank.STRAIGHT, "rank = %s" % rank)

    def testLowRanking(self):
	"""Verify ranking for low hand."""
	rank = PokerRank(Hand.fromString("AS 8C 7S 4D 3H"), lowRank=True)
	self.assertEqual(rank, PokerRank.HIGH_CARD, "%s != HIGH_CARD" % rank)
	self.assertEqual(rank.primaryCard, Rank.EIGHT,
			 "%s != 8, kickers = %s" % (rank.primaryCard,
						    rank.kickers))

    def testRanking(self):
	"""Test basic hand ranking."""
	hands = Hands()
	#
	# List in ascending order, so that if any hand compares greated than
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

	ranks = [PokerRank(hand) for hand in hands]
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
			    
				 
    def testOmaha(self):
	"""Test basic Omaha hand ranking."""
	hand = OmahaHand.fromString("7S QD 2D TD")
	board = Board.fromString("AS AD 4H TH 8D")
	hand.setBoard(board)
	rank = PokerRank(hand)
	self.assertEqual(rank, PokerRank.TWO_PAIR, "rank = %s" % rank)
	self.assertEqual(rank.primaryCard, Rank.ACE,
			 "primaryCard = %s" % rank.primaryCard )
	self.assertEqual(rank.secondaryCard, Rank.TEN,
			 "secondaryCard = %s" % rank.secondaryCard)

    def testOmaha2(self):
	"""Test Omaha low hand ranking."""
	hand = OmahaHand.fromString("5D 6H 9H 3C")
	board = Board.fromString("4H 6C JH KH 8C")
	hand.setBoard(board)
	rank = PokerRank.lowRank(hand)
	self.assertEqual(rank, PokerRank.HIGH_CARD, "rank = %s" % rank)
	self.assertEqual(rank.primaryCard, Rank.EIGHT,
			 "primaryCard = %s kickers = %s" % (rank.primaryCard,
							    rank.kickers))

if __name__ == "__main__":
    unittest.main()
