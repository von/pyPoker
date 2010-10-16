#!/usr/bin/env python
"""Unittests for PokerGame module"""

import StringIO
import unittest

from pyPoker import HoldEm
from pyPoker.Cards import Cards, Rank
from pyPoker.Deck import Deck
from pyPoker.Hand import Board
from pyPoker.Hands import Hands
from pyPoker.LowRanker import LowRanker
from pyPoker.Player import Player, Table
from pyPoker.PokerGame import \
    Action, InvalidActionException, \
    MessageHandler, Pot, Result, Simulator, Stats
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

    def test_MessageHander(self):
        """Test the MessageHandler class"""
        buffer = StringIO.StringIO()
        handler = MessageHandler(Table(), console=buffer)
        s = "Hello world"
        handler.message(s)
        self.assertEqual(buffer.getvalue(), s + "\n")
        s2 = "Hello again"
        handler.debug(s2)
        self.assertEqual(buffer.getvalue(), s + "\n" + "DEBUG: " + s2 + "\n")

    def test_Pot(self):
        """Test Pot class"""
        player_one = Player(name="One")
        player_two = Player(name="Two")
        player_three = Player(name="Three")
        player_four = Player(name="Four")
        contending_players = [player_one, player_two, player_three, player_four]
        pot = Pot(contending_players)
        self.assertIsNotNone(pot)
        self.assertEqual(pot.amount, 0)  # Default amount
        self.assertIsNone(pot.parent)
        self.assertListEqual(pot.contending_players, contending_players)
        pot.fold_player(player_one)
        contending_players.remove(player_one)
        self.assertListEqual(pot.contending_players, contending_players)
        self.assertIn(player_one, pot.folded_players)
        pot.amount += 100
        s = str(pot)
        self.assertIsInstance(s, str)
        self.assertEqual(s, "Main pot 100 (contenders: Two,Three,Four)")
        contending_players.remove(player_three)
        pot.new_side_pot(contending_players)
        self.assertListEqual(pot.contending_players, contending_players)  
        self.assertEqual(pot.amount, 0)      
        self.assertIsNotNone(pot.parent)
        self.assertEqual(pot.parent.amount, 100)
        # Should remove from both pot and pot.parent
        pot.fold_player(player_four)
        self.assertListEqual(pot.contending_players, [player_two])
        self.assertNotIn(player_four, pot.parent.contending_players)
        self.assertIn(player_four, pot.parent.folded_players)
        s = str(pot)
        self.assertIsInstance(s, str)
        self.assertEqual(s, "Side pot 0 (contenders: Two)")

    def test_Pot_new_side_pot(self):
        """Test Pot.new_side_pot() method"""
        player_one = Player(name="One")
        player_two = Player(name="Two")
        player_three = Player(name="Three")
        player_four = Player(name="Four")
        contending_players = [player_one, player_two, player_three, player_four]
        pot = Pot(contending_players)
        player_one.bet = 100
        player_two.bet = 0
        player_three.bet = 120
        player_four.bet = 90
        pot.new_side_pot()
        # Should have dropped player_two since .bet == 0
        self.assertListEqual(pot.contending_players,
                             [player_one, player_three, player_four])

    def test_Pot_pull_bets(self):
        """Test Pot.pull_bets() method"""
        player_one = Player(name="One")
        player_two = Player(name="Two")
        player_three = Player(name="Three")
        player_four = Player(name="Four")
        contending_players = [player_one, player_two, player_three, player_four]
        pot = Pot(contending_players)
        player_one.bet = 100
        player_two.bet = 10
        player_three.bet = 120
        player_four.bet = 90
        pot.pull_bets(maximum_pull=50)
        self.assertEqual(pot.amount, 160)
        self.assertEqual(player_one.bet, 50)
        self.assertEqual(player_two.bet, 0)
        self.assertEqual(player_three.bet, 70)
        self.assertEqual(player_four.bet, 40)
        pot.fold_player(player_one)  # Should still pull from this player
        pot.pull_bets()  # Should pull everything
        self.assertEqual(pot.amount, 320)
        for player in contending_players:
            self.assertEqual(player.bet, 0,
                             "%s bet == %d != 0" % (player, player.bet))

    def test_Pot_distribute(self):
        """Test Pot.distribute() method"""
        player_one = Player(name="One")
        player_two = Player(name="Two")
        player_three = Player(name="Three")
        player_four = Player(name="Four")
        contending_players = [player_one, player_two, player_three, player_four]
        pot = Pot(contending_players)
        pot.amount = 200
        pot.distribute(high_winners = [player_two])
        self.assertEqual(pot.amount, 0)
        self.assertEqual(player_two.stack, 200)
        for player in contending_players:
            player.stack = 0
        pot.amount = 200
        pot.distribute(high_winners = [player_one], low_winners = [player_four])
        self.assertEqual(pot.amount, 0)
        self.assertEqual(player_one.stack, 100)
        self.assertEqual(player_four.stack, 100)
        for player in contending_players:
            player.stack = 0
        pot.amount = 200
        pot.distribute(high_winners = [player_one, player_two],
                       low_winners = [player_three])
        self.assertEqual(pot.amount, 0)
        self.assertEqual(player_one.stack, 50)
        self.assertEqual(player_two.stack, 50)
        self.assertEqual(player_three.stack, 100)

if __name__ == "__main__":
    unittest.main()
