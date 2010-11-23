"""Module for classes representing a PokerGame player and table of players"""

import random
import sys

from Action import Action, InvalidActionException
from Hand import Hand
from PokerException import PokerException
from Utils import assertInstance, UserSelection

######################################################################
#
# Exceptions
#

class PlayerAlreadySeatedException(PokerException):
    """Player is already seated at this table."""
    pass

class SeatFullException(PokerException):
    """Seat is already taken."""
    pass

class TableFullException(PokerException):
    """Table is full."""
    pass

class ZeroStackException(PokerException):
    """Player's stack is zero."""
    pass

######################################################################

class Player(object):
    """Interface to a player in a game.

    Contains state related to player for a particular game and
    logic for interfacing with the player (be that a human or
    code)."""

    STATUS_SITTING_OUT = 0x01
    STATUS_ACTIVE = 0x02
    STATUS_ALL_IN = 0x03
    STATUS_FOLDED = 0x04

    STATUS_STRINGS = {
        STATUS_SITTING_OUT : "sitting out",
        STATUS_ACTIVE : "active",
        STATUS_ALL_IN : "all_in",
        STATUS_FOLDED : "folded",
        }

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

    def get_public_hand_as_str(self):
        """Return a string with the players hand as viewed publicly"""
        return self._hand.get_public_string()
            
    def make_active(self):
        """Make the player active. Stack must be non-zero."""
        if self.stack == 0:
            raise ZeroStackException()
        self.status = self.STATUS_ACTIVE

    def sit_out(self):
        """Change player's status to sitting out."""
        self.status = self.STATUS_SITTING_OUT

    def get_status(self):
        """Return status as string"""
        return self.STATUS_STRINGS[self.status]

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

    def get_action(self, request, game, hand_state):
        """Get a players betting action.

        Returns a Action instance."""
        if request.is_ante_request():
            action = self.get_ante_action(request, game, hand_state)
        elif request.is_blind_request():
            action = self.get_blind_action(request, game, hand_state)
        elif request.is_opening_bet_request():
            action = self.get_opening_bet_action(request, game, hand_state)
        elif request.is_call_request():
            action = self.get_call_action(request, game, hand_state)
        elif request.is_option_request():
            action = self.get_option_action(request, game, hand_state)
        else:
            raise ValueError("Unrecognized ActionRequest: {}".format(request))
        return action

    def get_ante_action(self, request, game, hand_state):
        """Get Action in response to ante request"""
        return Action.new_ante(min(request.amount, self.stack),
                               all_in = request.amount >= self.stack)

    def get_blind_action(self, request, game, hand_state):
        """Get Action in response to blind request"""
        return Action.new_blind(min(request.amount, self.stack),
                                all_in = request.amount >= self.stack)

    def get_opening_bet_action(self, request, game, hand_state):
        """Get Action in response to opening bet request"""
        # No bet required, check 75%, bet 25%
        random_number = random.random()
        if random_number < .75:
            action = Action.new_check()
        else:
            action = Action.new_bet(min(request.amount, self.stack),
                                    all_in=request.amount >= self.stack)
        return action

    def get_call_action(self, request, game, hand_state):
        """Get Action in response to call request"""
        # Bet in front of us, fold 50%, call 35%, raise 15% (if allowed)
        random_number = random.random()
        if (random_number < .15) and \
                (request.raise_amount is not None) and \
                (self.stack > request.amount):
            action = Action.new_raise(min(request.raise_amount, self.stack),
                                      all_in=request.raise_amount >= self.stack)
        elif random_number < .50:
            action = Action.new_call(min(request.amount, self.stack),
                                     all_in=request.amount >= self.stack)
        else:
            action = Action.new_fold()
        return action

    def get_option_action(self, request, game, hand_state):
        """Get Action in request to option request"""
        # Calls in front of us, raise 25%, check 75%
        random_number = random.random()
        if (random_number < .25) and \
                (self.stack > 0):
            action = Action.new_raise(min(request.raise_amount, self.stack),
                                      all_in=request.raise_amount >= self.stack)
        else:
            action = Action.new_check()
        return action

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

######################################################################

class HumanPlayer(Player):
    """Interface to a human player.

    >>> player=HumanPlayer("Jane", stack=1000, input=sys.stdin, output=sys.stdout)
    >>> str(player)
    'Jane'
    >>> player.stack
    1000
    """

    def __init__(self, name=None, stack=0, HandClass=Hand,
                 input=sys.stdin, output=sys.stdout):
        """Create an interface to human player using given input
        and output streams."""
        self.input = input
        self.output = output
        Player.__init__(self, name, stack, HandClass)

    def get_opening_bet_action(self, request, game, hand_state):
        """Get Action in response to open bet request"""
        self.display_hand_state(request, game, hand_state)
        user_selection = self._newUserSelection()
        user_selection.add_option("c", "check", Action.new_check())
        user_selection.add_option("b", "bet", Action.new_bet(request.amount))
        return user_selection.get_user_selection()

    def get_call_action(self, request, game, hand_state):
        """Get Action in response to call request"""
        self.display_hand_state(request, game, hand_state)
        user_selection = self._newUserSelection()
        user_selection.add_option("c",
                                  "call {}".format(request.amount),
                                  Action.new_call(request.amount))
        user_selection.add_option("f", "fold", Action.new_fold())
        if request.raise_amount != None:
            user_selection.add_option(\
                "r",
                "raise to {}".format(request.raise_amount),
                Action.new_raise(request.raise_amount))
        return user_selection.get_user_selection()

    def display_hand_state(self, request, game, hand_state):
        """Display current hand state to player"""
        self.message("Pot: {}".format(hand_state.pot))
        self.display_players(game, hand_state)
        self.display_hand(game, hand_state) 

    def display_players(self, game, hand_state):
        """Display other players at the table"""
        # Start at player after myself and go around table
        player = game.table.get_next_player(self)
        while player is not self:
            self.display_player(player)
            player = game.table.get_next_player(player)

    def display_player(self, player):
        """Display given player"""
        player_str = "{0}: Stack: {0.stack}".format(player)
        if player.is_sitting_out():
            self.message("{} - Sitting out".format(player_str))
        elif player.is_folded():
            self.message("{} - Folded".format(player_str))
        else:
            all_in_str = "(ALL-IN)" if player.is_all_in() else ""
            self.message("{} Bet: {} {} Hand: {}"\
                             .format(player_str,
                                     player.bet,
                                     all_in_str,
                                     player.get_public_hand_as_str()))

    def display_hand(self, game, hand_state):
        """Display players hand"""
        rank_strs = []
        if game.HighRanker is not None:
            high_rank = game.HighRanker.rankHand(self._hand)
            rank_strs.append("High: {}".format(high_rank))
        if game.LowRanker is not None:
            low_rank = game.LowRanker.rankHand(self._hand)
            rank_strs.append("Low: {}".format(low_rank))
        self.message("Your hand: {} ({})".format(self._hand,
                                                 " ".join(rank_strs)))
                     
    def message(self, string):
        """Handle a message to the player."""
        self.output.write(string.rstrip() + "\n")

    def _newUserSelection(self):
        """Return a new UserSelection instance"""
        return UserSelection(input_stream=self.input,
                             output_stream=self.output)

######################################################################

class Table(object):
    """Collection of players at a table"""

    def __init__(self, number_of_seats=9, players=None):
        """Create a table with given number of seats.

        Seat array of players if given."""
        assertInstance(number_of_seats, int)
        self.number_of_seats = number_of_seats
        # One extra seat for seat 0 which we don't use to keep
        # indexing simple.
        self.players = [ None ] * (number_of_seats + 1)
        if players is not None:
            self.seat_players(players)
        self.dealer = None

    def seat_player(self, player, seat_number=None):
        """Seat the given player.

        If seat_number is given, seat player there, otherwise chose randomly."""
        if player in self.players:
            raise PlayerAlreadySeatedException(
                "Player %s is already seated" % player)
        if seat_number is None:
            empty_seats = self.get_empty_seats()
            if len(empty_seats) == 0:
                raise TableFullException()
            seat_number = random.choice(empty_seats)
        else:
            if self.players[seat_number] is not None:
                raise SeatFullException()
        self.players[seat_number] = player

    def seat_players(self, players, in_order=False):
        """Randomly seat the given players.

        If in_order is True, seat in order at lowest numbered seats."""
        if in_order:
            empty_seats = self.get_empty_seats()
            for player in players:
                if len(empty_seats) == 0:
                    raise TableFullException()
                self.seat_player(player, seat_number=empty_seats.pop(0))
        else:
            for player in players:
                self.seat_player(player)

    def get_seated_players(self):
        """Return an array of seated players"""
        return filter(lambda p: p is not None, self.players)

    def get_player_seat(self, player):
        """Given a player return their seat number"""
        return self.players.index(player)

    def get_player_by_seat(self, seat):
        """Given a seat number, return the player sitting there"""
        return self.players[seat]

    def get_empty_seats(self):
        """Return an array of seat numbers which are empty"""
        return filter(lambda n: self.players[n] is None,
                      range(1, len(self.players)))

    def get_active_players(self):
        """Return an array of players who are active in the hand.

        This means players are not sitting out or have folded."""
        return filter(lambda p: p.is_active() or p.is_all_in(),
                      self.get_seated_players())

    def get_next_player(self, starting_player, filter=None):
        """Return the next player clockwise from given player.

        If filter is not none, it should be a function used to filter
        out players. If it returns False, player will be skipped. If
        no players passes filter, IndexError is raised.

        May return given player if logic so dictates."""
        starting_seat = self.get_player_seat(starting_player)
        seat = (starting_seat + 1) % len(self.players)
        while True:
            if (self.players[seat] is not None) and \
                    ((filter is None) or filter(self.players[seat])):
                break
            if seat == starting_seat:
                # We've go all the way around without a match
                raise IndexError()
            seat = (seat + 1) % len(self.players)
        return self.players[seat]

    def random_dealer(self):
        """Make a random player the dealer."""
        # XXX Should we choose a player with a non-zero stack?
        self.dealer = random.choice(self.get_seated_players())

    def set_dealer(self, player):
        """Set the dealer to the given player."""
        self.dealer = player

    def get_dealer(self):
        """Return the current dealer"""
        return self.dealer

    def advance_dealer(self):
        """Advance the dealer to the next player"""
        # XXX Should we choose a player with a non-zero stack?
        try:
            self.dealer = self.get_next_player(self.dealer)
        except IndexError:
            # No other player available, leave button where it is
            pass

    def __str__(self):
        player_strings = []
        for seat, player in enumerate(self.players):
            if player is None:
                continue
            s = "%d: %s" % (seat, player)
            if player == self.get_dealer():
                s+= "*"
            player_strings.append(s)
        return " ".join(player_strings)
            
