"""Classes for representing betting actions"""

from PokerException import PokerException

######################################################################
#
# Exceptions
#

class InvalidActionException(PokerException):
    """Action is invalid."""
    pass

######################################################################

class Action(object):
    """An action by a player (fold, check, call, bet, raise, ante, blind)"""

    TYPE_FOLD = 0x00
    TYPE_CHECK = 0x01
    TYPE_CALL = 0x02
    TYPE_BET = 0x03
    TYPE_RAISE = 0x04
    TYPE_BLIND = 0x05
    TYPE_ANTE = 0x06

    __strs = {
        TYPE_FOLD : "fold",
        TYPE_CHECK : "check",
        TYPE_CALL : "call",
        TYPE_BET : "bet",
        TYPE_RAISE : "raise",
        TYPE_BLIND : "blind",
        TYPE_ANTE : "ante",
        }

    def __init__(self, type, amount=0, all_in=False):
        """Create a Action.

        type must be one of the TYPE_* constants.

        amount must be the amount of the action. For a raise, it must be the
        total bet.

        all_in must be True if this represents an all-in.
        """
        # Todo: Sanity check arguments
        self.type = type
        self.amount = amount
        self.all_in = all_in

    #
    # Creation methods
    #

    @classmethod
    def new_ante(cls, amount, all_in=False):
        """Create a new ante action"""
        return Action(cls.TYPE_ANTE, amount=amount, all_in=all_in)

    @classmethod
    def new_bet(cls, amount, all_in=False):
        """Create a new bet action"""
        return Action(cls.TYPE_BET, amount=amount, all_in=all_in)

    @classmethod
    def new_blind(cls, amount, all_in=False):
        """Create a new blind action"""
        return Action(cls.TYPE_BLIND, amount=amount, all_in=all_in)

    @classmethod
    def new_call(cls, amount, all_in=False):
        """Create a new call action"""
        return Action(cls.TYPE_CALL, amount=amount, all_in=all_in)

    @classmethod
    def new_check(cls):
        """Create a new check action"""
        return Action(cls.TYPE_CHECK)

    @classmethod
    def new_fold(cls):
        """Create a new fold action"""
        return Action(cls.TYPE_FOLD)

    @classmethod
    def new_raise(cls, amount, all_in=False):
        """Create a new raise action"""
        return Action(cls.TYPE_RAISE, amount=amount, all_in=all_in)

    def is_all_in(self):
        """Does this action represent an all-in?"""
        return self.all_in

    #
    # Testing methods
    #

    def is_ante(self):
        """Is this action an ante?"""
        return self.type == self.TYPE_ANTE

    def is_bet(self):
        """Is this action a bet?"""
        return self.type == self.TYPE_BET

    def is_blind(self):
        """Is this action a blind?"""
        return self.type == self.TYPE_BLIND

    def is_call(self):
        """Is this action a call?"""
        return self.type == self.TYPE_CALL

    def is_check(self):
        """Is this action a check?"""
        return self.type == self.TYPE_CHECK

    def is_fold(self):
        """Is this action a fold?"""
        return self.type == self.TYPE_FOLD

    def is_raise(self):
        """Is this action a raise?"""
        return self.type == self.TYPE_RAISE

    def __str__(self):
        s = self.__strs[self.type]
        if self.amount:
            s += " %d" % self.amount
        if self.all_in:
            s += " (all-in)"
        return s
