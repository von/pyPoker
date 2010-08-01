#!/usr/bin/env python
######################################################################
#
# Unittests for PokerRank module
#
# $Id$
######################################################################

from pyPoker.Cards import Rank, Cards
from pyPoker.Hand import Hand, Board, OmahaHand, HoldEmHand
from pyPoker.Hands import Hands
from pyPoker.PokerRank import PokerRankBase, PokerRank, PokerLowRank
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testCreation(self):
        """Test basic creation of PokerRankBase."""
        kickers = Cards.fromString("JC 8D 4S")
        rank = PokerRankBase(PokerRank.PAIR, primaryCard=Rank.KING,
                             kickers=kickers)
        type = rank.getType()
        self.assertEqual(type, PokerRank.PAIR,
                         "rank = (%s) %d != PAIR" % (str(type), type))
        primaryRank = rank.getPrimaryCardRank()
        self.assertEqual(primaryRank, Rank.KING,
                         "primary rank = %s (%d) != KING" % (str(primaryRank),
                                                             primaryRank))
        secondaryRank = rank.getSecondaryCardRank()
        # Manual test here, otherwise string creation fails on sucess
        if secondaryRank is not None:
            self.fail("rank = %s (%d) != None" % (str(secondaryRank),
                                                  secondaryRank))
        kickerRanks = rank.getKickerRanks()
        for i, card in enumerate(kickers):
            self.assertEqual(card.rank, kickerRanks[i])

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

    def testBasicLowRanking(self):
	"""Verify ranking for low hand."""
	rank = PokerLowRank(Hand.fromString("AS 8C 7S 4D 3H"))
	self.assertEqual(rank, PokerRank.HIGH_CARD, "%s != HIGH_CARD" % rank)
	self.assertEqual(rank.getPrimaryCardRank(), Rank.EIGHT,
			 "%s != 8, kickers = %s" % (rank.getPrimaryCardRank(),
						    rank.kickersAsString()))
	self.assertEqual(rank.isEightOrBetter(), True,
			 "\"%s\".isEightOrBetter() != True" % rank)
        kickers = rank.getKickerRanks()
        self.assertEqual(len(kickers), 4,
                         "len(kickers) = %d != 4" % len(kickers))
        self.assertEqual(kickers[0], Rank.SEVEN,
                         "kickers[0] = %s != SEVEN" % kickers[0])
        self.assertEqual(kickers[1], Rank.FOUR,
                         "kickers[1] = %s != FOUR" % kickers[1])
        self.assertEqual(kickers[2], Rank.THREE,
                         "kickers[2] = %s != THREE" % kickers[2])
        self.assertEqual(kickers[3], Rank.ACE_LOW,
                         "kickers[3] = %s != ACE (low)" % kickers[3])

    def testRanking(self):
	"""Test basic hand ranking."""
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
		# King-high (ace is low)
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


	ranks = [PokerLowRank(hand) for hand in hands]
	for i in range(len(hands)):
	    for j in range(len(hands)):
		if (i < j):
		    self.assert_(ranks[i] < ranks[j],
				 "!(%d) %s (%s) < (%d) %s (%s)" %
				 ( i, hands[i], ranks[i].debugString(),
				   j, hands[j], ranks[j].debugString()))
		elif (i > j):
		    self.assert_(ranks[i] > ranks[j],
				 "!(%d) %s (%s) > (%d) %s (%s)" %
				 ( i, hands[i], ranks[i].debugString(),
				   j, hands[j], ranks[j].debugString()))
		else:
		    self.assertEqual(ranks[i], ranks[j],
				     "(%d) %s (%s) != (%d) %s (%s)" %
				     ( i, hands[i], ranks[i].debugString(),
				       j, hands[j], ranks[j].debugString()))
				 
    def testOmaha(self):
	"""Test basic Omaha hand ranking."""
	hand = OmahaHand.fromString("7S QD 2D TD")
	board = Board.fromString("AS AD 4H TH 8D")
	hand.setBoard(board)
	rank = PokerRank(hand)
	self.assertEqual(rank, PokerRank.TWO_PAIR, "rank = %s" % rank)
	self.assertEqual(rank.getPrimaryCardRank(), Rank.ACE,
			 "primaryCard = %s" % rank.getPrimaryCardRank())
	self.assertEqual(rank.getSecondaryCardRank(), Rank.TEN,
			 "secondaryCard = %s" % rank.getSecondaryCardRank())

    def testOmahaLow(self):
	"""Test Omaha low hand ranking."""
	hand = OmahaHand.fromString("5D 6H 9H 3C")
	board = Board.fromString("4H 6C JH KH 8C")
	hand.setBoard(board)
	rank = PokerLowRank(hand)
	self.assertEqual(rank, PokerRank.HIGH_CARD, "rank = %s" % rank)
	self.assertEqual(rank.getPrimaryCardRank(), Rank.EIGHT,
			 "primaryCard = %s kickers = %s" % (rank.getPrimaryCardRank(),
							    rank.kickersAsString()))

    def testOmahaLow2(self):
	"""Test Omaha low hand ranking."""
	hand = OmahaHand.fromString("QC AH TC 8C")
	board = Board.fromString("2H JH 4D 6H 3H")
	hand.setBoard(board)
	rank = PokerLowRank(hand)
	self.assertEqual(rank, PokerRank.HIGH_CARD, "rank = %s" % rank)
	self.assertEqual(rank.getPrimaryCardRank(), Rank.EIGHT,
			 "primaryCard = %s kickers = %s" % (rank.getPrimaryCardRank(),
							    rank.kickersAsString()))

if __name__ == "__main__":
    unittest.main()
