#!/usr/bin/env python
"""Unittests for PokerRank module"""

from pyPoker.Cards import Rank, Cards
from pyPoker.Hand import Hand, OmahaHand
from pyPoker.Hands import Hands
from pyPoker.PokerRank import PokerRank
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testCreation(self):
        """Test basic creation of PokerRankBase."""
        kickers = Cards.fromString("JC 8D 4S")
        rank = PokerRank(PokerRank.PAIR, primaryCard=Rank.KING,
                         kickers=kickers)
        self.assertIsNotNone(rank)
        self.assertNotEqual(rank, 0)
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

    def testKickerSort(self):
        """Test sorting of kickers."""
        kickers = Cards.fromString("8C KS AH")
        rank = PokerRank.pair(Rank.QUEEN, kickers)
        kickerRanks = rank.getKickerRanks()
        self.assertEqual(kickerRanks[0], Rank.ACE,
                         "kickerRanks[0] == %s != A" % kickerRanks[0])
        self.assertEqual(kickerRanks[1], Rank.KING,
                         "kickerRanks[1] == %s != K" % kickerRanks[1])
        self.assertEqual(kickerRanks[2], Rank.EIGHT,
                         "kickerRanks[2] == %s != 8" % kickerRanks[2])
        # Now test with Ace low
        kickers.makeAcesLow()
        rank = PokerRank.pair(Rank.QUEEN, kickers)
        kickerRanks = rank.getKickerRanks()
        self.assertEqual(kickerRanks[0], Rank.KING,
                         "kickerRanks[0] == %s != K" % kickerRanks[0])
        self.assertEqual(kickerRanks[1], Rank.EIGHT,
                         "kickerRanks[1] == %s != 8" % kickerRanks[1])
        self.assertEqual(kickerRanks[2], Rank.ACE_LOW,
                         "kickerRanks[2] == %s != A" % kickerRanks[2])

if __name__ == "__main__":
    unittest.main()
