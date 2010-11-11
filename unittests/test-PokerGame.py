#!/usr/bin/env python
"""Unittests for PokerGame module"""

import StringIO
import unittest

from pyPoker import HoldEm
from pyPoker.Action import Action, ActionRequest, InvalidActionException
from pyPoker.Cards import Cards, Rank
from pyPoker.Deck import Deck
from pyPoker.Hand import Board, Hand
from pyPoker.Hands import Hands
from pyPoker.LowRanker import LowRanker
from pyPoker.Player import Player, Table
from pyPoker.PokerGame import \
    BettingRound, HandState, \
    Game, MessageHandler, Pot, \
    Result, Simulator, Stats, Structure, \
    PokerGameStateException
from pyPoker.PokerRank import PokerRank
from pyPoker.Ranker import Ranker

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        # For message handlers
        self.console = file("/tmp/pypoker-console.log", "a")

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

    def test_BettingRound(self):
        """Test BettingRound class"""
        players = [ Player(stack=1000),
                    Player(stack=1000),
                    Player(stack=1000),
                    Player(stack=1000) ]
        table = Table()
        table.seat_players(players, in_order=True)
        message_handler = MessageHandler(table, self.console)
        pot = Pot(players)
        round = BettingRound(table, pot, message_handler)
        self.assertIsNotNone(round)
        self.assertEqual(round.table, table)
        self.assertEqual(round.pot, pot)
        self.assertRaises(PokerGameStateException, round.get_action_player)
        action_is_on = players[1]
        round.set_action(action_is_on)
        self.assertEqual(round.get_action_player(), action_is_on)
        self.assertIsNone(round.last_to_bet)
        self.assertEqual(len(round.action_record), 0)
        self.assertEqual(round.action_to_next_player(), players[2])
        self.assertEqual(round.action_to_next_player(), players[3])
        self.assertEqual(round.action_to_next_player(), players[0])
        self.assertEqual(round.action_to_next_player(), players[1])
        self.assertEqual(round.required_to_call(players[0]), 0)
        self.assertFalse(round.is_pot_good())
        # Have all players ante
        round.process_action(Action.new_ante(5))
        self.assertEqual(players[1].stack, 995)
        self.assertEqual(round.get_action_player(), players[2])
        self.assertEqual(round.last_to_bet, players[1])
        round.process_action(Action.new_ante(5))
        self.assertEqual(players[2].stack, 995)
        self.assertEqual(round.get_action_player(), players[3])
        self.assertEqual(round.last_to_bet, players[1])
        round.process_action(Action.new_ante(5))
        self.assertEqual(players[3].stack, 995)
        self.assertEqual(round.get_action_player(), players[0])
        self.assertEqual(round.last_to_bet, players[1])
        round.process_action(Action.new_ante(5))
        self.assertEqual(players[0].stack, 995)
        self.assertEqual(round.get_action_player(), players[1])
        self.assertEqual(round.last_to_bet, players[1])
        self.assertTrue(round.is_pot_good())
        self.assertEqual(round.sweep_bets_into_pot(), pot)
        self.assertEqual(pot.amount, 20)
        # New round
        round = BettingRound(table, pot, message_handler)
        self.assertIsNotNone(round)
        round.set_action(action_is_on)
        # Player 1 blinds, 2 blinds, 3 fold, 0 raises to 300
        round.process_action(Action.new_blind(50))
        self.assertEqual(players[1].bet, 50)
        round.process_action(Action.new_blind(100))
        round.process_action(Action.new_fold())
        self.assertTrue(players[3].is_folded())
        round.process_action(Action.new_raise(300))
        self.assertFalse(round.is_pot_good())
        self.assertEqual(round.get_action_player(), players[1])
        self.assertEqual(len(round.action_record), 4)
        self.assertEqual(round.total_pot(), 470)
        # Player 1 calls, 2 raises all in, 3 has folded, 0 folds
        self.assertEqual(round.required_to_call(), 250)
        round.process_action(Action.new_call(250))
        self.assertEqual(round.required_to_call(), 200)
        round.process_action(Action.new_raise(895, all_in=True))
        self.assertTrue(players[2].is_all_in())
        # Make sure we skipped player 3 who folded earlier
        self.assertEqual(round.get_action_player(), players[0])
        self.assertEqual(round.required_to_call(), 695)
        round.process_action(Action.new_fold())
        self.assertFalse(round.is_pot_good())
        self.assertEqual(round.total_pot(), 1615)
        # Plater 1 calls and pot should be good
        self.assertEqual(round.required_to_call(), 695)
        round.process_action(Action.new_call(695, all_in=True))
        self.assertTrue(round.is_pot_good())
        self.assertEqual(round.total_pot(), 2310)
        round.sweep_bets_into_pot()
        # Should only be main pot
        self.assertIsNone(pot.parent)
        # All players bets should have beet swept into pot
        for player in players:
            self.assertEqual(0, player.bet,
                             "Bet for %s == %d != 0" % (player, player.bet))
        self.assertEqual(pot.amount, 2310)

    def test_BettingRound_with_side_pots(self):
        """Test of BettingRound with side pots."""
        players = [ Player(stack=500),
                    Player(stack=100),
                    Player(stack=1000),
                    Player(stack=700) ]
        table = Table()
        table.seat_players(players, in_order=True)
        message_handler = MessageHandler(table, self.console)
        pot = Pot(players)
        round = BettingRound(table, pot, message_handler)
        action_is_on = players[0]
        round.set_action(action_is_on)
        # Player 0 50 blind, player 1 100 blind (allin),
        # player 2 raises to 300, player 4 calls
        round.process_action(Action.new_blind(50))
        round.process_action(Action.new_blind(100, all_in=True))
        round.process_action(Action.new_raise(300))
        round.process_action(Action.new_call(300))
        # Player 0 raises 450 all-in, player 2 raises 700 all-in
        # Player 3 folds
        round.process_action(Action.new_raise(450, all_in=True))
        # Make sure player 1, who is all-in, is skipped
        self.assertEqual(round.get_action_player(), players[2])
        round.process_action(Action.new_raise(700, all_in=True))
        round.process_action(Action.new_fold())
        self.assertTrue(round.is_pot_good())
        round.sweep_bets_into_pot()
        # At this point we should have a main point with 400
        # between 0,1 and 2, a side pot with 1000 between players 0 and 2,
        # and a side pot of 500 with just player 2.
        side_pot1 = round.pot
        self.assertEqual(side_pot1.amount, 500)
        self.assertListEqual(side_pot1.contending_players, [players[2]])
        self.assertIsNotNone(side_pot1.parent)

    def test_BettingRound_blind_walk(self):
        """Test of BettingRound with a walk for the blind"""
        players = [ Player(stack=500),
                    Player(stack=100),
                    Player(stack=1000),
                    Player(stack=700) ]
        table = Table()
        table.seat_players(players, in_order=True)
        message_handler = MessageHandler(table, self.console)
        pot = Pot(players)
        round = BettingRound(table, pot, message_handler)
        action_is_on = players[0]
        round.set_action(action_is_on)
        # Player 0 50 blind, fold, fold, fold
        round.process_action(Action.new_blind(50))
        round.process_action(Action.new_fold())
        round.process_action(Action.new_fold())
        round.process_action(Action.new_fold())
        self.assertTrue(round.is_pot_good())
        round.sweep_bets_into_pot()
        # At this point we should have a pot of 50 with only player
        # 0 contending.
        pot = round.pot
        self.assertEqual(pot.amount, 50)
        self.assertListEqual(pot.contending_players, [players[0]])
        self.assertIsNone(pot.parent)

    def test_HandState(self):
        """Test HandState class"""
        players = [ Player(stack=500),
                    Player(stack=100),
                    Player(stack=1000),
                    Player(stack=700) ]
        table = Table()
        table.seat_players(players, in_order=True)
        message_handler = MessageHandler(table, self.console)
        hand_state = HandState(table, message_handler)
        self.assertIsNotNone(hand_state)
        self.assertEqual(hand_state.table, table)
        for player in players:
            self.assertIsNotNone(player._hand)
        hand_state.deal_cards(5)
        for player in players:
            self.assertEqual(len(player._hand), 5)
        betting_round = hand_state.new_betting_round()
        self.assertIsNotNone(betting_round)
        self.assertEqual(hand_state.get_current_betting_round(), betting_round)
        self.assertEqual(len(hand_state.betting_rounds), 1)
        betting_round2 = hand_state.new_betting_round()
        self.assertIsNotNone(betting_round2)
        self.assertEqual(hand_state.get_current_betting_round(), betting_round2)
        self.assertEqual(len(hand_state.betting_rounds), 2)
        self.assertIsNotNone(hand_state.dump_to_string())

    def test_Structure_limit(self):
        """Test a Limit Structure class"""
        ante = 10
        blinds = [50,100]
        min_bets = [100,100,200,200]
        structure = Structure(Structure.LIMIT, ante=ante,
                              blinds=blinds, bet_sizes=min_bets)
        self.assertIsNotNone(structure)
        self.assertTrue(structure.is_limit())
        self.assertFalse(structure.is_pot_limit())
        self.assertFalse(structure.is_no_limit())
        self.assertEqual(structure.get_ante(), ante)
        self.assertListEqual(structure.get_blinds(), blinds)
        betting_round = 1
        self.assertEqual(
            structure.get_minimum_bet(betting_round=betting_round),
            min_bets[betting_round-1])

    def test_Structure_pot_limit(self):
        """Test a Limit Structure class"""
        ante = 0
        blinds = [10,20]
        structure = Structure(Structure.POT_LIMIT, ante=ante, blinds=blinds)
        self.assertIsNotNone(structure)
        self.assertFalse(structure.is_limit())
        self.assertTrue(structure.is_pot_limit())
        self.assertFalse(structure.is_no_limit())
        self.assertEqual(structure.get_ante(), ante)
        self.assertListEqual(structure.get_blinds(), blinds)
        # minimum bet should be big blind for all rounds
        betting_round = 1
        self.assertEqual(structure.get_minimum_bet(betting_round=betting_round),
                         max(blinds))

    def test_Structure_no_limit(self):
        """Test a Limit Structure class"""
        ante = 5
        blinds = [10]
        structure = Structure(Structure.LIMIT, ante=ante, blinds=blinds)
        self.assertIsNotNone(structure)
        self.assertTrue(structure.is_limit())
        self.assertEqual(structure.get_ante(), ante)
        self.assertListEqual(structure.get_blinds(), blinds)
        # minimum bet should be big blind for all rounds
        betting_round = 1
        self.assertEqual(structure.get_minimum_bet(betting_round=betting_round),
                         max(blinds))

    def test_Game(self):
        """Test Game class"""
        players = [
            Player(name="Player One", stack=1000),
            Player(name="Player Two", stack=1000),
            Player(name="Player Three", stack=1000)
            ]
        table = Table(players = players)
        structure = Structure(Structure.LIMIT, ante=5, blinds=[10])
        game = Game(table, structure, console=self.console)
        self.assertIsNotNone(game)
        self.assertEqual(game.table, table)
        self.assertEqual(game.structure, structure)
        # Default MessageHander should be created.
        self.assertIsNotNone(game.message_handler)
        game.message("Test message")
        game.debug("Test debug message")
        # Simulate play_hand()
        hand_state = HandState(table, game.message_handler)
        game.antes(hand_state)
        self.assertEqual(hand_state.pot.amount, 15)
        game.action_to_left_of_dealer(hand_state)
        betting_round = hand_state.get_current_betting_round()
        self.assertIsInstance(betting_round, BettingRound)
        self.assertIsInstance(betting_round.get_action_player(), Player)
        game.blinds(hand_state)
        self.assertEqual(betting_round.total_pot(), 25)  # Antes + 10 blind
        game.deal_hands(hand_state)
        for player in players:
            self.assertEqual(len(player._hand), 5)
        # Simulate betting_round()
        self.assertFalse(betting_round.is_pot_good())
        action_request = game._get_action_request(hand_state)
        self.assertIsInstance(action_request, ActionRequest)
        # Should be call of blind
        self.assertTrue(action_request.is_call_request())
        self.assertEqual(action_request.amount, 10)
        self.assertEqual(action_request.raise_amount, 20)
        # Fold UTG
        betting_round.process_action(Action.new_fold())
        self.assertFalse(betting_round.is_pot_good())
        # Should be same request as before
        action_request2 = game._get_action_request(hand_state)
        self.assertIsInstance(action_request2, ActionRequest)
        self.assertTrue(action_request2.is_call_request())
        self.assertEqual(action_request2.amount, 10)
        self.assertEqual(action_request2.raise_amount, 20)
        # Now raise
        betting_round.process_action(Action.new_raise(20))
        self.assertFalse(betting_round.is_pot_good())
        # Action back on blind
        action_request3 = game._get_action_request(hand_state)
        self.assertIsInstance(action_request3, ActionRequest)
        self.assertTrue(action_request3.is_call_request())
        self.assertEqual(action_request3.amount, 10)
        self.assertEqual(action_request3.raise_amount, 20)
        betting_round.process_action(Action.new_call(10))
        self.assertTrue(betting_round.is_pot_good())
        game.pot_to_high_hand(hand_state)

    def test_Game_play_hand(self):
        """Test Game.play_hand() method"""
        players = [ Player(name="Player One", stack=1000) ]
        table = Table(players = players)
        self.assertEqual(len(table.get_active_players()), 1)
        structure = Structure(Structure.LIMIT, ante=5, blinds=[10])
        game = Game(table, structure, console=self.console)
        # Trying to play a hand with only one player should be an exception
        with self.assertRaises(PokerGameStateException):
            game.play_hand()
        table.seat_players([
            Player(name="Player Two", stack=1000),
            Player(name="Player Three", stack=1000)
            ])
        self.assertEqual(len(table.get_active_players()), 3)
        hand_state = game.play_hand()
        self.assertIsInstance(hand_state, HandState)
        # Make sure all players states have been reset
        for player in table.get_seated_players():
            if player.stack > 0:
                self.assertTrue(player.is_active())
            else:
                self.assertTrue(player.is_sitting_out())

if __name__ == "__main__":
    unittest.main()
