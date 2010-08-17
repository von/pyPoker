#!/usr/bin/env python
"""Unittests for HoldEm module"""

from pyPoker import HoldEm
from pyPoker.Cards import Cards, Rank
from pyPoker.Hand import Board
from pyPoker.PokerRank import PokerRank
from pyPoker.slanskyHands import SlanskyHand

import unittest

class TestSequenceFunctions(unittest.TestCase):

    def testHands(self):
	hands = HoldEm.Hands()
	hands.addHandGroup("AKs")
	self.assertEquals(len(hands), 4)
	hands.__str__()
	hands.addHandGroup("JT")
	self.assertEquals(len(hands), 16)
	hands.__str__()
	hands.addAllHands(Rank.SEVEN, Rank.NINE)
	self.assertEquals(len(hands), 32)
	hands.__str__()
	hands.addPair(Rank.SIX)
	self.assertEquals(len(hands), 38)
	hands.__str__()
	hands.addSuitedAceXHands()
	self.assertEquals(len(hands), 70)
	hands.__str__()
	hands.addSuitedKingXHands()
	self.assertEquals(len(hands), 102)
	hands.__str__()

    def testGame(self):
	"""Test HoleEmGame."""
	game = HoldEm.Game()
	game.setBoard(Board.fromString("5C 2S 4D"))
	game.addHand(HoldEm.Hand.fromString("AC 2C"))
	game.addHand(HoldEm.Hand.fromString("AH KH"))
	game.simulateGames(numGames=10)

    def testGameHandGenerator(self):
	"""Test Game with HandGenerator."""
	game = HoldEm.Game()
	game.addHand(HoldEm.Hand.fromString("AC 2C"))
	game.addHand(HoldEm.Hand.fromString("AH KH"))
	game.addHandGenerator(HoldEm.HandGenerator(SlanskyHand['class1']))
	game.addHandGenerator(HoldEm.HandGenerator(SlanskyHand['class2']))
	game.addHandGenerator(HoldEm.HandGenerator(SlanskyHand['class3']))
	game.addHandGenerator(HoldEm.HandGenerator(SlanskyHand['class4']))
	game.simulateGames(numGames=10)


    def testHoldEmStartingHandRanker(self):
        """Test basic ranking (high card)."""
        ranker = HoldEm.StartingHandRanker()
        rank = ranker.rankHand(Cards.fromString("2C 8D"))
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
        ranker = HoldEm.StartingHandRanker()
        rank = ranker.rankHand(Cards.fromString("5C 5D"))
        self.assertIsNotNone(rank)
        self.assertIsInstance(rank, PokerRank)
        self.assertNotEqual(rank, 0)
        self.assertEqual(rank.getType(), PokerRank.PAIR)
        self.assertEqual(rank.getPrimaryCardRank(), Rank.FIVE)
        kickers = rank.getKickerRanks()
        self.assertEqual(len(kickers), 0)

if __name__ == "__main__":
    unittest.main()
