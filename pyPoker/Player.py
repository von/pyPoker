"""Module for classes representing a PokerGame player"""

from Hand import Hand
from PokerGame import Action, InvalidActionException

class Player(object):
    """Interface to a player in a game.

    Contains state related to player for a particular game and
    logic for interfacing with the player (be that a human or
    code)."""

    STATUS_SITTING_OUT = 0x01
    STATUS_ACTIVE = 0x02
    STATUS_ALL_IN = 0x03
    STATUS_FOLDED = 0x04

    def __init__(self, name=None, stack=0, HandClass=Hand):
        if name is None:
            name = "Unnamed Player"
        self.name = name
        self.stack = stack
        self.HandClass = HandClass
        # Amount bet in current hand not yet swept into pot
        self.bet = 0
        if self.stack > 0:
            self.status = self.STATUS_ACTIVE
        else:
            self.status = self.STATUS_SITTING_OUT
        # Private state
        self._hand = None

    def new_hand(self):
        """Create a new hand for player, setting status to active"""
        self.muck_hand()
        self._hand = self.HandClass()
        self.status = self.STATUS_ACTIVE

    def deal_card(self, deck):
        """Deal the player a card from the given deck"""
        deck.deal(self._hand)

    def muck_hand(self):
        """Muck the player's hand, setting player's status to folded"""
        self._hand = None
        self.status = self.STATUS_FOLDED

    def is_sitting_out(self):
        """Is the player sitting out?"""
        return (self.status == self.STATUS_SITTING_OUT)

    def is_active(self):
        """Is the player still actively betting?"""
        return (self.status == self.STATUS_ACTIVE)

    def is_all_in(self):
        """Is the player all-in?"""
        return (self.status == self.STATUS_ALL_IN)

    def is_folded(self):
        """Is the player folded?"""
        return (self.status == self.STATUS_FOLDED)

    def get_action(self, game, hand_state):
        """Get a players betting action.

        Returns a Action instance."""
        raise NotImplementedException()

    def message(self, string):
        """Handle a message to the player.

        This implementation just discards it."""
        pass

    def process_action(self, action):
        """Move amount of action from stack to bet.

        If action is an all-in, verify that is the case."""
        if action.amount < 0:
            raise InvalidActionException("Action is negative")
        if action.amount > self.stack:
            raise InvalidActionException("Bet is larger than player stack")
        if action.is_all_in() and (action.amount != self.stack):
            raise InvalidActionException("All-in action is not size of stack")
        self.stack -= action.amount
        self.bet += action.amount

    def win(self, amount):
        """Add given winings to stack"""
        self.stack += amount

    def __str__(self):
        return self.name


