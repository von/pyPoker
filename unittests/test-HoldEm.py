#!/usr/bin/env python
"""Unittests for HoldEm module"""

from pyPoker import HoldEm
from pyPoker.Cards import Cards, Rank
from pyPoker.Deck import Deck
from pyPoker.Hand import Board
from pyPoker.Hands import Hands
from pyPoker.PokerGame import Result, Stats
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

    def test_Simulator(self):
        """Test HoldEm.Simulator"""
        simulator = HoldEm.Simulator()
        self.assertIsNotNone(simulator)
        self.assertEqual(simulator.GAME_NAME, "Texas Hold'em")
        result = simulator.simulate_game()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        stats = simulator.simulate_games(number_of_games=4)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, Stats)

    def test_Simulator_with_predefined(self):
        """Test Simulator with HoldEm hands and board"""
        deck = Deck()
        board = Board()
        deck.dealHands(board)
        hands = deck.createHands(9, handClass=HoldEm.Hand)
        simulator = HoldEm.Simulator(predefined_hands=hands,
                                     predefined_board=board)
        self.assertIsNotNone(simulator)
        result = simulator.simulate_game()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        stats = simulator.simulate_games(number_of_games=4)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, Stats)
        
    def test_Simulator_with_HandGenerator(self):
	"""Test Simulator with HandGenerator."""
        hands = Hands()
        hands.addHand(HoldEm.Hand.fromString("AC 2C"))
	hands.addHand(HoldEm.Hand.fromString("AH KH"))
	hands.addHand(HoldEm.HandGenerator(SlanskyHand['class1']))
	hands.addHand(HoldEm.HandGenerator(SlanskyHand['class2']))
	hands.addHand(HoldEm.HandGenerator(SlanskyHand['class3']))
	hands.addHand(HoldEm.HandGenerator(SlanskyHand['class4']))
	simulator = HoldEm.Simulator(predefined_hands=hands)
        simulator.simulate_games(number_of_games=10)

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
