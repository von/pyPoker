#!/usr/bin/env python
"""Unittests for player module"""

import unittest

from pyPoker.Deck import Deck
from pyPoker.Player import Player
from pyPoker.PokerGame import Action, InvalidActionException

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
        player2 = Player(stack=10)
        self.assertEqual(str(player2), "Unnamed Player")
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
        """Test deal_card() method"""
        player = Player()
        deck = Deck()
        player.new_hand()
        self.assertIsNotNone(player._hand)
        player.deal_card(deck)
        self.assertEqual(len(player._hand), 1)
        self.assertEqual(len(deck), 51)

if __name__ == "__main__":
    unittest.main()
