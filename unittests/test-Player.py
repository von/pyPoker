#!/usr/bin/env python
"""Unittests for player module"""

import unittest

from pyPoker.Action import Action, InvalidActionException
from pyPoker.Deck import Deck
from pyPoker.Player import Player, Table, \
    PlayerAlreadySeatedException, \
    SeatFullException, \
    TableFullException, \
    ZeroStackException

class TestSequenceFunctions(unittest.TestCase):

    def test_new_Player(self):
        """Test basic Player construction."""
        jane = Player(name = "Jane")
        self.assertIsNotNone(jane)
        self.assertEqual(str(jane), "Jane")
        phil = Player(name = "Phil")
        self.assertIsNotNone(phil)
        self.assertEqual(str(phil), "Phil")

    def test_Player(self):
        """Test Player class"""
        player = Player(name="Bob")
        self.assertIsNotNone(player)
        self.assertEqual(str(player), "Bob")
        self.assertTrue(player.is_sitting_out())
        with self.assertRaises(ZeroStackException):
            player.make_active()
        player2 = Player(stack=10)
        self.assertEqual(str(player2), "Unnamed Player")
        self.assertTrue(player2.is_active())
        player2.sit_out()
        self.assertTrue(player2.is_sitting_out())
        player2.make_active()
        self.assertTrue(player2.is_active())
        player.new_hand()
        self.assertTrue(player.is_active())
        player.muck_hand()
        self.assertTrue(player.is_folded())
        player.message("This should go nowhere")
        player.stack = 100
        action = Action.new_bet(30)
        player.process_action(action)
        self.assertEqual(player.stack, 70)
        self.assertEqual(player.bet, 30)
        action = Action.new_bet(100)
        self.assertRaises(InvalidActionException, player.process_action, action)
        player.win(10)
        self.assertEqual(player.stack, 80)

    def test_deal_card(self):
        """Test Player.deal_card() method"""
        player = Player()
        deck = Deck()
        player.new_hand()
        self.assertIsNotNone(player._hand)
        player.deal_card(deck)
        self.assertEqual(len(player._hand), 1)
        self.assertEqual(len(deck), 51)

    def test_Table(self):
        """Test Table class"""
        table = Table()
        self.assertIsNotNone(table)
        self.assertEqual(table.number_of_seats, 9)
        self.assertEqual(len(table.players), 10)  # 9 + 1
        player = Player()
        table.seat_player(player, seat_number = 4)
        self.assertEqual(table.get_player_by_seat(4), player)
        self.assertEqual(table.get_player_seat(player), 4)
        self.assertEqual(len(table.get_seated_players()), 1)
        self.assertEqual(len(table.get_empty_seats()), 8)
        self.assertRaises(PlayerAlreadySeatedException,
                          table.seat_player, player)
        players = [ Player(), Player(), Player(), Player() ]
        table.seat_players(players)
        self.assertEqual(len(table.get_seated_players()), 5)
        self.assertEqual(len(table.get_empty_seats()), 4)
        player2 = Player()
        table.seat_player(player2)
        self.assertEqual(len(table.get_seated_players()), 6)
        self.assertEqual(len(table.get_empty_seats()), 3)
        player3 = Player()
        self.assertRaises(SeatFullException,
                          table.seat_player, player3, 4)
        players2 = [ Player(), Player(), Player(), Player() ]
        self.assertRaises(TableFullException,
                          table.seat_players, players2)
        table.random_dealer()
        self.assertIn(table.get_dealer(), table.get_seated_players())
        table.advance_dealer()
        self.assertIsInstance(table.__str__(), str)

    def test_Table_get_active_players(self):
        """Test Table.get_active_players() method."""
        players = [ Player(stack=100), Player(stack=100),
                    Player(stack=100), Player(stack=0) ]
        table = Table(players=players)
        active_players = table.get_active_players()
        # players[3] shouldn't be in players since they are sitting out
        # with stack == 0
        self.assertIsNotNone(active_players)
        self.assertEqual(len(active_players), 3)
        self.assertNotIn(players[3], active_players)

    def test_Table_get_next_player(self):
        """Test Table.get_next_player() method."""
        players = [ Player(name="One", stack=100),
                    Player(name="Two", stack=200),
                    Player(name="Three", stack=500),
                    Player(name="Four", stack=0)
                    ]
        table = Table()
        table.seat_players(players, in_order=True)
        self.assertEqual(table.get_next_player(players[0]), players[1])
        self.assertEqual(table.get_next_player(players[1]), players[2])
        self.assertEqual(table.get_next_player(players[2]), players[3])
        self.assertEqual(table.get_next_player(players[3]), players[0])
        self.assertEqual(
            table.get_next_player(players[0], filter=lambda p: p.stack > 300),
            players[2])
        table.set_dealer(players[1])
        self.assertEqual(table.get_dealer(), players[1])
        self.assertEqual(str(table), "1: One 2: Two* 3: Three 4: Four")
                                               
if __name__ == "__main__":
    unittest.main()
