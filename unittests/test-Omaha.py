#!/usr/bin/env python
"""Unittests for Omaha module"""

from pyPoker.Deck import Deck
from pyPoker.Hand import Board
from pyPoker import Omaha
from pyPoker.PokerGame import Result, Stats

import testing

class TestSequenceFunctions(testing.TestCase):

    def testLowPossible(self):
        """Test eightLowPossible() method"""
        # These hands have a possible low
	for hand in [ "AC 2C 3C 4D",
		      "AC AD 2C 2D",
		      "7C 8C 9C TC",
		      "AC 8C JC KC" ]:
	    self.assertEqual(Omaha.Hand.fromString(hand).eightLowPossible(),
			     True, "%s not True" % hand)
        # These hands don't have a possible low
	for hand in [ "AC AH AS 9D",
		      "AC AD 9C TD",
		      "7C 9C TC KC",
		      "AC 9C JC KC" ]:
	    self.assertEqual(Omaha.Hand.fromString(hand).eightLowPossible(),
			     False, "%s not False" % hand)

    def testCombinations(self):
	"""Testing Omaha combinations."""
	hand = Omaha.Hand.fromString("AC 2C 3C 4C");
	board = Board.fromString("5C 6C 7C 8C 9C");
	hand.setBoard(board)
        self.assert_iterator(hand.combinations(2), count=6,
                             assert_item_function=lambda i: len(i) == 2)
        self.assert_iterator(hand.hands(), count=60,
                             assert_item_function=lambda i: len(i) == 5)

    def test_combinations_of_eight_or_lower(self):
        """Test combinations_of_eight_or_lower() method on hand with board"""
        # Hand doesn't have two low cards, can't make low
        hand = Omaha.Hand.fromString("AD 9D JS QS")
	board = Board.fromString("3D 4D 5D")
	hand.setBoard(board)
        self.assert_iterator(hand.combinations_of_eight_or_lower(5),
                             count=0)
        # Board doesn't have three low cards, can't make low
        hand = Omaha.Hand.fromString("AD 9D 7D QS")
	board = Board.fromString("3D KD 5D")
	hand.setBoard(board)
        self.assert_iterator(hand.combinations_of_eight_or_lower(5),
                             count=0)
        # Three low cards in hand, 3 on board == 3 possible lows
        hand = Omaha.Hand.fromString("AD 9D 7D 8S")
	board = Board.fromString("3D 4D 5D")
	hand.setBoard(board)
        self.assert_iterator(hand.combinations_of_eight_or_lower(5),
                             count=3,
                             assert_item_function=lambda i: len(i)==5)
        # Two low cards in hand, 3 on board == 1 possible low
        hand = Omaha.Hand.fromString("AD 9D 7D QS")
	board = Board.fromString("3D 4D 5D")
	hand.setBoard(board)
        self.assert_iterator(hand.combinations_of_eight_or_lower(5),
                             count=1,
                             assert_item_function=lambda i: len(i)==5)
        # Add a low card to the board for 2 in hand, 4 on board == 4 combos
	board.addCardFromString("6D")
        self.assert_iterator(hand.combinations_of_eight_or_lower(5),
                             count=4,
                             assert_item_function=lambda i: len(i)==5)
        # Add a high card to board, should have no change
	board.addCardFromString("TD")
        self.assert_iterator(hand.combinations_of_eight_or_lower(5),
                             count=4,
                             assert_item_function=lambda i: len(i)==5)

    def testPoints(self):
	"""Test Omaha HiLo point scoring."""
	hands = {
	    "AC AD 2C 3D":95,
	    "AC KH QD JS":16,
	    "AC AD KH KS":45,
	    "KS 2S QH 3H":22,
	    "AC AH AD 4H":35,
	    "AC 2C 3C 4H":74,
	    "7C 8C 9C TC":12
	    }
	for hand in hands.keys():
	    value = Omaha.Hand.fromString(hand).pointValue()
	    self.assertEquals(value, hands[hand],
			      "%s == %d != %d points" % (hand, value, 
							 hands[hand]))

    def test_Simulator(self):
        """Test HoldEm.Simulator"""
        simulator = Omaha.Simulator()
        self.assertIsNotNone(simulator)
        self.assertEqual(simulator.GAME_NAME, "Omaha")
        result = simulator.simulate_game()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        stats = simulator.simulate_games(number_of_games=4)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, Stats)

    def test_HiLoSimulator(self):
        """Test HoldEm.HiLoSimulator"""
        simulator = Omaha.HiLoSimulator()
        self.assertIsNotNone(simulator)
        self.assertEqual(simulator.GAME_NAME, "Omaha Hi/Lo 8-or-better")
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
        hands = deck.createHands(9, handClass=Omaha.Hand)
        simulator = Omaha.Simulator(predefined_hands=hands,
                                    predefined_board=board)
        self.assertIsNotNone(simulator)
        result = simulator.simulate_game()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Result)
        stats = simulator.simulate_games(number_of_games=4)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, Stats)

if __name__ == "__main__":
    testing.main()
