#!/usr/bin/env python
"""Unittests for Action module"""

import testing

from pyPoker.Action import Action, ActionRequest, InvalidActionException

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

    def test_ActionRequest(self):
        """Test ActionRequest class"""
        request = ActionRequest(ActionRequest.ANTE_REQUEST, 10)
        self.assertIsNotNone(request)
        self.assertTrue(request.is_ante_request())
        self.assertEqual(request.amount, 10)
        self.assertEqual(str(request), "ante request for 10")
        request.validate_action(Action.new_ante(10))

    def test_ante_ActionRequest(self):
        """Test ActionRequest for ante"""
        amount = 20
        request = ActionRequest.new_ante_request(amount)
        self.assertIsNotNone(request)
        self.assertTrue(request.is_ante_request())
        self.assertEqual(request.amount, amount)
        request.validate_action(Action.new_ante(amount))
        request.validate_action(Action.new_fold())
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_ante(amount+1))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_call(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_bet(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_raise(amount))

    def test_blind_ActionRequest(self):
        """Test ActionRequest for blind"""
        amount = 50
        request = ActionRequest.new_blind_request(amount)
        self.assertIsNotNone(request)
        self.assertTrue(request.is_blind_request())
        self.assertEqual(request.amount, amount)
        request.validate_action(Action.new_blind(amount))
        request.validate_action(Action.new_fold())
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_blind(amount+1))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_call(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_bet(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_raise(amount))

    def test_opening_bet_ActionRequest(self):
        """Test ActionRequest for opening bet"""
        amount = 50
        request = ActionRequest.new_opening_bet_request(amount)
        self.assertIsNotNone(request)
        self.assertTrue(request.is_opening_bet_request())
        self.assertEqual(request.amount, amount)
        request.validate_action(Action.new_check())
        request.validate_action(Action.new_bet(amount))
        request.validate_action(Action.new_fold())
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_ante(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_blind(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_call(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_bet(amount+1))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_raise(amount))

    def test_call_ActionRequest(self):
        """Test ActionRequest for call"""
        amount = 50
        request = ActionRequest.new_call_request(amount, raise_amount=amount*2)
        self.assertIsNotNone(request)
        self.assertTrue(request.is_call_request())
        self.assertEqual(request.amount, amount)
        self.assertEqual(request.raise_amount, amount*2)
        self.assertEqual(str(request), "call request for 50 or raise of 100")
        request.validate_action(Action.new_call(amount))
        request.validate_action(Action.new_raise(amount*2))
        request.validate_action(Action.new_fold())
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_ante(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_blind(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_call(amount+1))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_bet(amount))
        with self.assertRaises(InvalidActionException):
            request.validate_action(Action.new_raise(amount*2-1))

if __name__ == "__main__":
    testing.main()
