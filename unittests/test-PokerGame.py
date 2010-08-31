#!/usr/bin/env python
"""Unittests for PokerGame module"""

import unittest

from pyPoker.Cards import Cards, Rank
from pyPoker.Deck import Deck
from pyPoker.Hands import Hands
from pyPoker.LowRanker import LowRanker
from pyPoker.PokerGame import PokerGame, Result, Stats
from pyPoker.PokerRank import PokerRank
from pyPoker.Ranker import Ranker

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def test_PokerGame(self):
        """Test basic PokerGame construction"""
        game = PokerGame()
        self.assertIsNotNone(game)

    def test_highHandWins(self):
        """Test highHandWins() method"""
        game = PokerGame()
        self.assertTrue(game.highHandWins())

    def test_lowHandWins(self):
        """Test lowHandWins() method"""
        game = PokerGame()
        self.assertFalse(game.lowHandWins())


    # Todo: Add some more PokerGame tests here
    # Right now PokerGame is implicitly tested by its child classes
    # (e.g. HoldEm.Game), but some explicit tests should be added.

    def test_Result(self):
        """Test basic construction and operation of Result instance"""
        deck = Deck()
        hands = deck.createHands(9)
        ranker = Ranker()
        high_winners, high_rank = ranker.bestHand(hands)
        low_ranker = LowRanker()
        low_winners, low_rank = low_ranker.bestHand(hands)
        result = Result(hands=hands,
                        high_winners=high_winners,
                        winning_high_rank=high_rank,
                        low_winners=low_winners,
                        winning_low_rank=low_rank)
        self.assertIsNotNone(result)
        self.assertListEqual(high_winners, result.high_winners)
        self.assertEqual(high_rank, result.winning_high_rank)
        self.assertListEqual(low_winners, result.low_winners)
        self.assertEqual(low_rank, result.winning_low_rank)
        self.assertListEqual(hands, result.hands)

    def test_Stats(self):
        """Test basic construction and operation of Stats instance"""
        stats = Stats()
        self.assertIsNotNone(stats)
        # Should have 9 players by default
        self.assertEqual(stats.number_of_hands, 9)
        # Test both direct attribute access and methods
        self.assertEqual(stats.number_of_games, 0)
        self.assertEqual(stats.get_number_of_games(), 0)
        self.assertEqual(len(stats.high_winners), stats.number_of_hands)
        self.assertEqual(len(stats.get_high_winners()), stats.number_of_hands)
        self.assertEqual(len(stats.low_winners), stats.number_of_hands)
        self.assertEqual(len(stats.get_low_winners()), stats.number_of_hands)
        self.assertEqual(len(stats.scoops), stats.number_of_hands)
        self.assertEqual(len(stats.get_scoops()), stats.number_of_hands)
        for index in range(stats.number_of_hands):
            self.assertEqual(0, stats.high_winners[index])
            self.assertEqual(0, stats.low_winners[index])
            self.assertEqual(0, stats.scoops[index])

    def test_record_game(self):
        """Test Stats.record_game() and Stats.reset()"""
        # Generate a result
        deck = Deck()
        hands = deck.createHands(9)
        ranker = Ranker()
        high_winners, high_rank = ranker.bestHand(hands)
        low_ranker = LowRanker()
        low_winners, low_rank = low_ranker.bestHand(hands)
        result = Result(hands=hands,
                        high_winners=high_winners,
                        winning_high_rank=high_rank,
                        low_winners=low_winners,
                        winning_low_rank=low_rank)
        stats = Stats()
        stats.record_game(result)
        self.assertEqual(stats.number_of_hands, 9)
        self.assertEqual(stats.number_of_games, 1)
        self.assertEqual(len(stats.high_winners), stats.number_of_hands)
        self.assertEqual(len(stats.low_winners), stats.number_of_hands)
        self.assertEqual(len(stats.scoops), stats.number_of_hands)
        # Figure out if we have a scooper
        if ((len(stats.high_winners) == 1) and
            (len(stats.low_winners) == 1) and
            (stats.high_winners[0] == stats.low_winners[0])):
            scooper = stats.low_winners[0]
        else:
            scooper = None
        for index in range(stats.number_of_hands):
            if index in high_winners:
                self.assertEqual(1, stats.high_winners[index])
            else:
                self.assertEqual(0, stats.high_winners[index])
            if index in low_winners:
                self.assertEqual(1, stats.low_winners[index])
            else:
                self.assertEqual(0, stats.low_winners[index])
            if (scooper is not None) and (scooper == index):
                self.assertEqual(1, stats.scoops[index])
            else:
                self.assertEqual(0, stats.scoops[index])
        # OK, now try reseting stats
        stats.reset()
        self.assertEqual(stats.number_of_games, 0)
        self.assertEqual(len(stats.high_winners), stats.number_of_hands)
        self.assertEqual(len(stats.low_winners), stats.number_of_hands)
        self.assertEqual(len(stats.scoops), stats.number_of_hands)
        for index in range(stats.number_of_hands):
            self.assertEqual(0, stats.high_winners[index])
            self.assertEqual(0, stats.low_winners[index])
            self.assertEqual(0, stats.scoops[index])

if __name__ == "__main__":
    unittest.main()
