#!/usr/bin/env python
"""Unittests for HoldEmStartingHandRanker module"""

from pyPoker.Cards import Cards, Rank
from pyPoker.HoldEmStartingHandRanker import HoldEmStartingHandRanker
from pyPoker.PokerRank import PokerRank
import unittest

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        self.ranker = HoldEmStartingHandRanker()

    def testHoldEmStartingHandRanker(self):
        """Test basic ranking (high card)."""
        rank = self.ranker.rankHand(Cards.fromString("2C 8D"))
        self.assertIsNotNone(rank)
        self.assertIsInstance(rank, PokerRank)
        self.assertNotEqual(rank, 0)
        self.assertEqual(rank.getType(), PokerRank.HIGH_CARD)
        self.assertEqual(rank.getPrimaryCardRank(), Rank.EIGHT)
        kickers = rank.getKickerRanks()
        self.assertEqual(len(kickers), 1)
        self.assertEqual(kickers[0], Rank.TWO)

    def testHoldEmStartingHandRanker2(self):
        """Test basic ranking (pair)."""
        rank = self.ranker.rankHand(Cards.fromString("5C 5D"))
        self.assertIsNotNone(rank)
        self.assertIsInstance(rank, PokerRank)
        self.assertNotEqual(rank, 0)
        self.assertEqual(rank.getType(), PokerRank.PAIR)
        self.assertEqual(rank.getPrimaryCardRank(), Rank.FIVE)
        kickers = rank.getKickerRanks()
        self.assertEqual(len(kickers), 0)

if __name__ == "__main__":
    unittest.main()
