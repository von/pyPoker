#!/usr/bin/env python
"""Unittests for Action module"""

import testing

from pyPoker.Action import Action, InvalidActionException

class TestSequenceFunctions(testing.TestCase):
    """Tests for Action module"""

    def setUp(self):
        pass


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
    testing.main()
