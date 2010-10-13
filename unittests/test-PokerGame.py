#!/usr/bin/env python
"""Unittests for PokerGame module"""

import unittest

from pyPoker import HoldEm
from pyPoker.Cards import Cards, Rank
from pyPoker.Deck import Deck
from pyPoker.Hand import Board
from pyPoker.Hands import Hands
from pyPoker.LowRanker import LowRanker
from pyPoker.PokerGame import \
    Action, InvalidActionException, \
    Result, Simulator, Stats
from pyPoker.PokerRank import PokerRank
from pyPoker.Ranker import Ranker

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def test_Simulator(self):
        """Test basic Simulator construction"""
        simulator = Simulator()
        self.assertIsNotNone(simulator)
        self.assertEqual(simulator.GAME_NAME, "Poker")
        simulator = Simulator(number_of_hands=10)
        self.assertIsNotNone(simulator)
        deck = Deck()
        hands = deck.createHands(9)
        simulator = Simulator(predefined_hands=hands)
        self.assertIsNotNone(simulator)
        self.assertEqual(hands, simulator.get_predefined_hands())

    def test_simulate_game(self):
        """Test Simulator.simulate_game()"""
        simulator = Simulator()
        result = simulator.simulate_game()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)

    def test_simulate_games(self):
        """Test Simulator.simulate_games()"""
        simulator = Simulator()
        stats = simulator.simulate_games()
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, Stats)

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

    def test_Action_ante(self):
        """Test ante Action"""
        action = Action.new_ante(1)
        self.assertIsNotNone(action)
        self.assertTrue(action.is_ante())
        self.assertEqual(action.amount, 1)
        self.assertFalse(action.is_all_in())
        self.assertEqual(str(action), "ante 1")

    def test_Action_bet(self):
        """Test bet Action"""
        action = Action.new_bet(100)
        self.assertIsNotNone(action)
        self.assertTrue(action.is_bet())
        self.assertFalse(action.is_raise())
        self.assertEqual(action.amount, 100)
        self.assertFalse(action.is_all_in())
        self.assertEqual(str(action), "bet 100")

    def test_Action_blind(self):
        """Test blind Action"""
        action = Action.new_blind(50)
        self.assertIsNotNone(action)
        self.assertTrue(action.is_blind())
        self.assertEqual(action.amount, 50)
        self.assertFalse(action.is_all_in())
        self.assertEqual(str(action), "blind 50")

    def test_Action_call(self):
        """Test call Action"""
        action = Action.new_call(200, all_in=True)
        self.assertIsNotNone(action)
        self.assertTrue(action.is_call())
        self.assertEqual(action.amount, 200)
        self.assertTrue(action.is_all_in())
        self.assertEqual(str(action), "call 200 (all-in)")

    def test_Action_check(self):
        """Test check Action"""
        action = Action.new_check()
        self.assertIsNotNone(action)
        self.assertTrue(action.is_check())
        self.assertEqual(action.amount, 0)
        self.assertFalse(action.is_all_in())
        self.assertEqual(str(action), "check")

    def test_Action_fold(self):
        """Test fold Action"""
        action = Action.new_fold()
        self.assertIsNotNone(action)
        self.assertTrue(action.is_fold())
        self.assertEqual(action.amount, 0)
        self.assertFalse(action.is_all_in())
        self.assertEqual(str(action), "fold")

    def test_Action_raise(self):
        """Test raise Action"""
        action = Action.new_raise(500, all_in=True)
        self.assertIsNotNone(action)
        self.assertTrue(action.is_raise())
        self.assertEqual(action.amount, 500)
        self.assertTrue(action.is_all_in())
        self.assertEqual(str(action), "raise 500 (all-in)")

    def test_InvalidActionException(self):
        """Test InvalidActionException"""
        def f():
            raise InvalidActionException()
        self.assertRaises(InvalidActionException, f)

if __name__ == "__main__":
    unittest.main()
