"""Class for simulating poker games."""

import copy
import itertools
import random

from Action import Action, ActionRequest
from PokerException import PokerException
from Hand import Hand, CommunityCardHand
from Hands import Hands
from Cards import Cards
from Deck import Deck
from Utils import assertInstance
from Ranker import Ranker
from LowRanker import LowRanker
from HandGenerator import HandGenerator

######################################################################
#
# Exceptions
#

class PokerGameStateException(PokerException):
    """Error in state for game simulation."""
    pass

class TooManyHandsException(PokerException):
    """Too many hands defined (not enough cards)."""
    pass

class InvalidBoardException(PokerException):
    """Board is invalid."""
    pass

######################################################################

class Simulator(object):
    """Simulate a poker game (no betting)"""

    # Class to use for Hands
    HandClass=Hand
    
    # Class to use for ranking high hands
    # Or None if high hand doesn't win
    HighRankerClass=Ranker

    # Class to use for rnaking low hands
    # Or None if low hand doesn't win
    LowRankerClass=None

    # String descrition of this game
    GAME_NAME="Poker"

    def __init__(self,
                 number_of_hands=9,
                 predefined_hands=None,
                 predefined_board=None):
        """Initialize simulation.

        number_of_hands is number of hands total to simulate.

        predefined_hands should be a Hands instances and can containe
        either Hand or HandGenerator instances. For a latter a new
        hand will be generated for each simulation.

        predefined_board should be a predefined set of community cards.
        Setting this for a HandClass that doesn't support a board will
        raise an error.
        """
        # Todo: add argument sanity checking
        if number_of_hands > self.getMaxHands():
            raise TooManyHandsException("Only %d hands allowed"
                                        % self.getMaxHands())
        self.number_of_hands = number_of_hands

        self.predefined_hands = predefined_hands
        if self.HighRankerClass is not None:
            self.high_ranker = self.HighRankerClass()
        else:
            self.high_ranker = None
        if self.LowRankerClass is not None:
            self.low_ranker = self.LowRankerClass()
        else:
            self.low_ranker = None
        self.board = None
        if issubclass(self.HandClass, CommunityCardHand):
            if predefined_board is None:
                BoardClass = self.HandClass.boardClass
                self.board = BoardClass()
            else:
                # Todo: verify board is of appropriate class
                self.board = predefined_board
        elif predefined_board is not None:
            raise InvalidBoardException("Given HandClass does not support a Board")
        self.deck = Deck()
        
    @classmethod
    def getMaxHands(cls):
        """Return the maximum number of hands that can be dealt"""
	cards_per_hand = cls.HandClass.maxCards
        cards_in_deck = 52
        if issubclass(cls.HandClass, CommunityCardHand):
            cards_in_deck -= cls.HandClass.boardClass.maxCards
	return int(cards_in_deck/cards_per_hand)

    def get_predefined_hands(self):
        """Return array of predefined hands or None if none predefined."""
        return self.predefined_hands

    def simulate_games(self,
                       number_of_games = 100,
                       callback=None, callbackArg=None,
                       stats=None):
        """Simulate a bunch of games with starting hands. Returns
	a array with number of wins for each hand.

        Returns a Stats instance with the statistics from the games. If a
        stats instance is passed in, the same one, augmented, will be
        returned.

        callback should be a function that takes the form:
        callback(game, result, *callbackarg)
        """
        assertInstance(number_of_games, int)
        if stats is None:
            stats = Stats(number_of_hands = self.number_of_hands)
	while number_of_games > 0:
	    result = self.simulate_game()
            stats.record_game(result)
	    if callback is not None:
                args = [self, result]
                if callbackArg is not None:
                    args.append(callbackArg)
                callback(*args)
            number_of_games -= 1
        return stats

    def simulate_game(self):
	# Make a copy of deck, hands and board
	deck = self.deck.copy()
	deck.shuffle()
	hands = Hands()
        # Deal out predefined hands
        if self.predefined_hands is not None:
            for hand in self.predefined_hands:
                if isinstance(hand, HandGenerator):
                    hands.addHand(hand.generateHand(deck = deck))
                else:
                    hands.addHand(hand.copy())
                    deck.removeCards(hand)
	# If we have less than numHands, fill it out
	while len(hands) < self.number_of_hands:
	    hands.addHand(self.HandClass())
	if self.board is None:
	    board = None
	else:
	    board = self.board.copy()
	# Fill out hands and board
	deck.dealHands(hands)
	if board is not None:
	    # Deal board
	    deck.dealHands(board)
	    for hand in hands:
		hand.setBoard(board)
        result = Result(hands, board=board)
	# Find winning hands
	if self.high_ranker is not None:
	    (high_winners, bestHighRank) = self.high_ranker.bestHand(hands)
            result.high_winners = high_winners
            result.winning_high_rank = bestHighRank
	if self.low_ranker is not None:
	    (low_winners, bestLowRank) = self.low_ranker.bestHand(hands)
            result.low_winners = low_winners
            result.winning_low_rank = bestLowRank
        return result

class Result(object):
    """Result from a hand of poker."""
    def __init__(self, hands, board=None,
                 high_winners=None, winning_high_rank=None,
                 low_winners=None, winning_low_rank=None):
        """Generate a Result object

        high_winners should be an array of indexes of winning high hands.
        winning_high_rank should be a Rank object representing the winning high rank.
        low_winners should be an array of indexes of winning low hands.
        winning_low_rank should be a Rank object representing the winning low rank.
        
        board should be a board, if used in game.

        hands should be a Hands instance with hands from game.

        Values can all be accessed directly."""
        self.high_winners = high_winners
        self.winning_high_rank = winning_high_rank
        self.low_winners = low_winners
        self.winning_low_rank = winning_low_rank
        self.board = board
        self.hands = hands
                 
class Stats(object):
    """Object from holding stats from a series of poker games."""

    def __init__(self, number_of_hands=9):
        self.number_of_hands = number_of_hands
        self.reset()

    def reset(self):
        """Reset statistics"""
        # For each hand, number of wins high
        self.high_winners = [0] * self.number_of_hands
        # For each hand, number of wins low
        self.low_winners = [0] * self.number_of_hands
        # For each hand, number of scoops (wins both ways)
        self.scoops = [0] * self.number_of_hands
        # How many games have we recorded?
        self.number_of_games = 0

    def record_game(self, results):
        """Record the winners of a game

        results should be a Results instance."""
        self.number_of_games += 1
        if results.high_winners is not None:
            for winner in results.high_winners:
                if winner >= len(self.high_winners):
                    raise IndexError(\
                        "High winner #%d larger than number of hands (%d)" %
                        (winner, self.number_of_hands))
                self.high_winners[winner] += 1
        if results.low_winners is not None:
            for winner in results.low_winners:
                if winner >= len(self.low_winners):
                    raise IndexError(\
                        "Low winner #%d larger than number of hands (%d)" %
                        (winner, self.number_of_hands))
                self.low_winners[winner] += 1
        # If we have one winner who won both high and low, we have a scooper
        if (results.low_winners is not None) and \
                (len(results.low_winners) == 1) and \
                (results.high_winners is not None) and \
                (len(results.high_winners) == 1) and \
                (results.low_winners[0] == results.high_winners[0]):
            self.scoops[results.low_winners[0]] += 1

    def get_number_of_games(self):
        """Return number of games recorded"""
        return self.number_of_games

    def get_number_of_hands(self):
        """Return number of hand in recorded games"""
        return self.number_of_hands

    def get_high_winners(self):
        """Return an array with number of high wins by each hand"""
        return self.high_winners

    def get_low_winners(self):
        """Return an array with number of low wins by each hand"""
        return self.low_winners

    def get_scoops(self):
        """Return an array with number of scoops by each hand"""
        return self.scoops

######################################################################

class Game(object):
    """Class holding all the state and logic for a Poker game with betting."""

    # Class to use for hands
    HandClass = Hand

    # Class for determining high hands
    HighRanker = Ranker

    # Class for determinging low winners
    LowRanker = None

    # Steps to playing a hand. This should be overriden by class classes.
    STEPS = [
        "antes",
        "action_to_left_of_dealer",
        "blinds",
        "deal_hands",
        "betting_round",
        "pot_to_high_hand",
        ]

    def __init__(self,
                 table,
                 structure,
                 console=None):
        """table must be a Table instance.

        structure must be a Structure instance represent game structure.

        console must be a stream to which a copy of all messages
        should be delivered or None if messages should be discarded.
        """
        # Todo: sanity check arguments
        self.table = table
        self.structure = structure
        self.message_handler = MessageHandler(table, console)
        table.random_dealer()
        self.message("New game")
        self.debug("Table: %s" % table)

    def report_action(self, player, action):
        """Report on the given action"""
        self.message("%s %s" % (player, action))

    def message(self, msg):
        """Handle a message about the game."""
        self.message_handler.message(msg)

    def debug(self, msg):
        """Handle a debug message about the game."""
        self.message_handler.debug(msg)

    def play_hand(self):
        """Play a hand."""
        if len(self.table.get_active_players()) < 2:
            raise PokerGameStateException(\
                "Need at least two active players to play a hand")
        self.message("New hand starting")
        hand_state = HandState(self.table, self.message_handler)
        for step in self.STEPS:
            self.debug("Hand step: %s" % step)
            code = "self.%s(hand_state)" % step
            eval(code)
        self.table.advance_dealer()
        return hand_state

    #
    # Methods that provide steps
    #

    def antes(self, hand_state):
        """Handle antes."""
        ante_amount = self.structure.get_ante()
        if ante_amount > 0:
            self.message("Collecting ante of %d" % ante_amount)
            active_players = self.table.get_active_players()
            betting = hand_state.new_betting_round()
            betting.set_action(active_players[0])
            request = ActionRequest.new_ante_request(ante_amount)
            for player in active_players:
                action = player.get_action(request, self, hand_state)
                request.validate_action(action)
                betting.process_action(action)
                self.report_action(player, action)
            betting.sweep_bets_into_pot()

    def action_to_left_of_dealer(self, hand_state):
        """Create new BettingRound and set action to dealer's left"""
        action_is_on = self.table.get_next_player(
            self.table.get_dealer(),
            filter=lambda p: p.is_active() and p.stack > 0)
        self.message("Action starts on %s" % action_is_on)
        round = hand_state.new_betting_round()
        round.set_action(action_is_on)

    def blinds(self, hand_state):
        """Handle blinds."""
        # XXX What if # blinds < # players?
        blinds = self.structure.get_blinds()
        betting = hand_state.get_current_betting_round()
        for blind in blinds:
            player = betting.get_action_player()
            if player.stack < blind:
                action = Action.new_blind(player.stack,
                                          all_in=True)
            else:
                action = Action.new_blind(blind)
            betting.process_action(action)
            self.report_action(player, action)

    def deal_hands(self, hand_state):
        """Deal full hands to all players."""
        hand_state.deal_cards(self.HandClass.maxCards)
        for player in self.table.get_active_players():
            self.debug("{}: {}".format(player, player._hand))

    def betting_round(self, hand_state):
        """Handle betting"""
        self.debug("Round of betting")
        betting_round = hand_state.get_current_betting_round()
        while not betting_round.is_pot_good():
            player = betting_round.get_action_player()
            request = self._get_action_request(hand_state)
            self.debug("Action is on {}: {}".format(player, request))
            action = player.get_action(request, self, hand_state)
            betting_round.process_action(action)
            self.report_action(player, action)
        betting_round.sweep_bets_into_pot()

    def pot_to_high_hand(self, hand_state):
        """Award pot to high hand using cls.HighRanker"""
        self.message("Awarding pot to best high hand")
        # First calculate high ranks for all plays with hands
        high_ranks = {}
        for player in self.table.get_active_players():
            high_ranks[player] = self.HighRanker.rankHand(player._hand)
            self.debug("{} has {} for a {}".format(player,
                                                   player._hand,
                                                   high_ranks[player]))
        # Now awarding pots starting with last side pot
        pot = hand_state.pot
        while pot is not None:
            winning_rank = max([high_ranks[p] for p in pot.contending_players])
            winning_players = filter(lambda p: high_ranks[p] == winning_rank,
                                     pot.contending_players)
            self.message("%s to %s with %s" % \
                             (pot,
                              ",".join([str(p) for p in winning_players]),
                              winning_rank))
            pot.distribute(high_winners = winning_players)
            pot = pot.parent

    def _get_action_request(self, hand_state):
        """Generate an ActionRequest for player whom action is currently on"""
        betting_round = hand_state.get_current_betting_round()
        required_to_call = betting_round.required_to_call()
        minimum_bet = self.structure.get_minimum_bet(betting_round)
        if required_to_call == 0:
            request = ActionRequest.new_opening_bet_request(minimum_bet)
        else:
            request = ActionRequest.new_call_request(\
                required_to_call,
                raise_amount = required_to_call + minimum_bet)
        return request

######################################################################

class Pot(object):
    """A pot (main or side) with list of contending players

    This implements a linked list of Pots, the first being the main
    pot and then a series of side pots with the last being the pot
    currently being bet into."""

    def __init__(self, contending_players, amount=0,
                 parent=None, message_handler=None):
        # Todo: Sanity check arguments
        if len(contending_players) < 1:
            raise ValueError("contending_players empty")
        self.contending_players = copy.copy(contending_players)
        self.folded_players = []
        self.parent = parent
        self.amount = amount
        self.message_handler = message_handler
        self._message("New " + str(self))

    def fold_player(self, player):
        """Fold a player, removing them from contention of this pot and any parent pots"""
        if player not in self.contending_players:
            raise ValueError("Attempt to fold player not contending for pot")
        self.contending_players.remove(player)
        self.folded_players.append(player)
        if self.parent: self.parent.fold_player(player)
        self._debug("Folding " + str(player))

    def pull_bets(self, maximum_pull=None):
        """Pull bets from all players who were or are in pot.

        If maximum_pull is not None, only pull up to max chips."""
        if maximum_pull is None:
            self._debug("Pulling bets (no maximum)")
        else:
            self._debug("Pulling bets (%d maximum)" % maximum_pull)
        for player in itertools.chain(self.contending_players,
                                      self.folded_players):
            if maximum_pull is not None:
                pull = min(maximum_pull, player.bet)
            else:
                pull = player.bet
            player.bet -= pull
            self.amount += pull

    def new_side_pot(self, contending_players=None):
        """Create a new side pot. This pot is saved as parent.

        contending_players should be an array of players who will be
        the contending players in the new side pot. If None, all contending
        players with a bet greater than 0 will be contenders."""
        if contending_players is None:
            contending_players = filter(lambda p: p.bet > 0,
                                        self.contending_players)
        # Todo: contending_players must be subset of self.contending_players
        new_parent = Pot(contending_players=contending_players,
                         amount=self.amount,
                         parent=self.parent)
        self.contending_players = contending_players
        self.parent = new_parent
        self.amount = 0

    def distribute(self, high_winners=None, low_winners=None):
        """Distribute pot among winning players."""
        # First split pot into halves if needed
        high = (high_winners is not None) and (len(high_winners) > 0)
        low = (low_winners is not None) and (len(low_winners) > 0)
        if not(high or low):
            raise ValueError("No winners given")
        if high and low:
            # XXX Need to deal with chip size and fraction going to high
            high_portion = self.amount/2
            low_portion = self.amount/2
        elif high:
            high_portion = self.amount
            low_portion = 0
        else:
            low_portion = self.amount
            high_portion = 0
        # Ok, now distribute
        if high_portion > 0:
            # XXX Need to deal with chip size and fraction going to
            #     worst position
            share = high_portion / len(high_winners)
            for player in high_winners:
                player.win(share)
        if low_portion > 0:
            # XXX Need to deal with chip size and fraction going to
            #     worst position
            share = low_portion / len(low_winners)
            for player in low_winners:
                player.win(share)
        self.amount = 0

    def __str__(self):
        if self.parent is None:
            s = "Main pot"
        else:
            s = "Side pot"
        s += " %d" % self.amount
        s += " (contenders: " + \
            ",".join([str(player) for player in self.contending_players]) + \
            ")"
        return s

    def _message(self, msg):
        """Handle a message"""
        if self.message_handler:
            self.message_handler.message(msg)

    def _debug(self, msg):
        """Handle a debug message"""
        if self.message_handler:
            self.message_handler.debug(msg)

######################################################################

class MessageHandler(object):
    """Handle messages from PokerGame

    This delivers messages to all players involved in a game plus a
    console intended for debugging."""

    def __init__(self, table, console=None):
        """Create a MessageHandler instance.

        players should be an array of Player instances to whom messages
        should be past.

        console should be a file descriptor to receive debug messages.
        If None, debug messages will be dropped.
        """
        self.table = table
        self.console = console
        
    def message(self, msg):
        """Deliver a message to all players and the console"""
        self._write_to_console(msg)
        for player in self.table.get_seated_players():
            player.message(msg)

    def debug(self, msg):
        """Handle a debug message only delivered to console."""
        self._write_to_console("DEBUG: " + msg)

    def _write_to_console(self, msg):
        # Assuming single-line message
        if self.console:
            self.console.write(msg.rstrip() + "\n")

######################################################################

class HandState(object):
    """State of a given hand.

    After creation, use process_action() to add actions. Complete processing
    with finish_processing() after which no more acctions should be processed.
    """

    def __init__(self, table, message_handler=None):
        """players should be array of players to be seated.

        deal must be the player who is the current dealer. If None, the
        lowest seated player will be the dealer.

        message handler must be a MessageHandler instance or None."""
        self.table = table
        self.message_handler = message_handler

        #
        # Private state not available to players
        #
        self._deck = Deck()
        self._deck.shuffle()

        active_players = self.table.get_active_players()

        # Create main pot to start with
        self.pot = Pot(contending_players = active_players)
        # Create initial hands
        for player in active_players:
            player.new_hand()
        # Record of betting rounds
        self.betting_rounds = []


    def deal_cards(self, number_of_cards=1):
        """Deal number_of_cards to each player."""
        for card in range(number_of_cards):
            for player in self.table.get_active_players():
                player.deal_card(self._deck)

    def new_betting_round(self):
        """Create a new betting round"""
        new_round = BettingRound(self.table,
                                   self.pot,
                                   message_handler=self.message_handler)
        self.betting_rounds.append(new_round)
        return new_round

    def get_current_betting_round(self):
        """Return the current betting round"""
        return self.betting_rounds[len(self.betting_rounds) - 1]

    def dump_to_string(self):
        """Dump our state to a string for debugging."""
        s = ""
        s += str(self.table)
        s += str(self.pot)
        s += "On betting round %d" % (len(self.betting_rounds) + 1)
        return s

    def _message(self, msg):
        """Handle a message"""
        if self.message_handler is not None:
            self.message_handler.message(msg)

    def _debug(self, msg):
        """Handle a debug message"""
        if self.message_handler is not None:
            self.message_handler.debug(msg)

######################################################################

class BettingRound(object):
    """State and logic associated with a round of betting."""

    def __init__(self, table, pot, message_handler=None):
        """
        pot must be a Pot instance that will be modified in place.
        
        action_is_on must a Player contending for pot
        indicating the player who is first to act.
        """
        self.table = table
        self.pot = pot
        self.message_handler = message_handler
        #
        # Who is the action on?
        self.action_is_on = None
        #
        # Last player to bet or raise
        self.last_to_bet = None
        #
        # Is pot good?
        self.pot_is_good = False
        #
        # Record of (player, actions)
        self.action_record = []
        self._debug("New BettingRound")

    def get_action_player(self):
        """Return the player whom the action is on"""
        if self.action_is_on is None:
            raise PokerGameStateException("Action has not been set")
        return self.action_is_on

    def set_action(self, player):
        """Set the action to the given player"""
        if player not in self.table.get_seated_players():
            raise ValueError("Player not at table")
        self.action_is_on = player

    def action_to_next_player(self):
        """Move action to the next active player.

        Sets pot_is_good to True if action is complete.

        Return index of new active player"""
        if self.action_is_on is None:
            raise PokeGameStateException(
                "Player whom action is on is not defined")
        try:
            self.action_is_on = \
                self.table.get_next_player(self.action_is_on,
                                           filter=lambda p: p.is_active())
        except IndexError:
            # No active players left, set action on last_to_bet to
            # trigger pot_is_good logic below
            self.action_is_on = self.last_to_bet
        if self.action_is_on is self.last_to_bet:
            # Action is back on last player to bet or raise,
            # pot is now good.
            self.pot_is_good = True
            self._message("Pot is good.")
        return self.action_is_on

    def is_pot_good(self):
        """Return true if the pot is good and betting is complete."""
        return self.pot_is_good

    def required_to_call(self, player=None):
        """How much does the given player have to put into the pot to call?

        If player is None, then the current player whom the action on
        is used."""
        if player is None:
            player = self.action_is_on
        return self.max_bet() - player.bet

    def total_pot(self, player=None):
        """What is the total of pots plus bets not swept into pot yet we are playing for?

        Only counts bets up to what player can contend for.

        If player is None, calculates for current player action is on."""
        if player is None:
            player = self.action_is_on
        bets = [player.bet for player in self.table.get_seated_players()]
        # Figure out total of bets that player can contend for
        bet_total = sum(map(lambda b: min(b, player.bet + player.stack), bets))
        return bet_total + self.pot.amount

    def process_action(self, action):
        """Process action for current player to act

        action must already have been valided per structure.

        Advances action to next player."""
        if self.action_is_on is None:
            raise PokeGameStateException(
                "Player whom action is on is not defined")
        player = self.action_is_on  # For convienence
        required_to_call = self.required_to_call(player)
        if action.is_ante():
            player.process_action(action)
            if self.last_to_bet is None:
                self.last_to_bet = player
        elif action.is_bet():
            if required_to_call > 0:
                raise InvalidActionException(\
                    "Bet not allowed when call required")
            player.process_action(action)
            self.last_to_bet = player
        elif action.is_blind():
            # Do not set last_to_bet here as a blind does not prevent
            # player from acting when betting comes back around to them.
            player.process_action(action)
        elif action.is_call():
            if (action.amount != required_to_call) and not action.is_all_in():
                raise InvalidActionException(\
                    "Call not of correct amount (%d)" % required_to_call)
            player.process_action(action)
            # Call of a blind counts as a bet
            if self.last_to_bet is None:
                self.last_to_bet = player
        elif action.is_check():
            if required_to_call > 0:
                raise InvalidActionException(\
                    "Check not allowed when call required")
            # An opening check counts as a bet of zero
            if self.last_to_bet is None:
                self.last_to_bet = player
        elif action.is_fold():
            self.pot.fold_player(player)
            player.status = player.STATUS_FOLDED
        elif action.is_raise():
            if (action.amount <= required_to_call) and not action.is_all_in():
                raise InvalidActionException("Raise too small")
            player.process_action(action)
            self.last_to_bet = player
        self.action_record.append((player, action))
        self._debug("Action: %s by %s" % (action, player))
        if action.is_all_in():
            player.status = player.STATUS_ALL_IN
        self.action_to_next_player()

    def sweep_bets_into_pot(self):
        """Complete processing, generating side pots as needed for all-ins.

        Returns Pot instance."""
        # All folded players have had their bets put into pot already
        # by process_action(), so we should only be dealing with live
        # players.
        if not self.is_pot_good():
            raise PokerGameStateException(
                "sweep_bets_into_pot() called before pot is good")
        self._debug("Sweeping bets into pot")
        # Loop until no play has money to be put into pot
        while self.max_bet() > 0:
            all_ins = filter(lambda p: p.is_all_in(), self.players_with_bets())
            if len(all_ins) == 0:
                # No all-ins, just sweep bets into pot
                self.pot.pull_bets()
                break
            else:
                # We have one or more all-ins.
                # Find the smallest all-in bet size
                smallest_all_in_bet_size = \
                    min([player.bet for player in all_ins])
                smallest_all_in_players = \
                    filter(lambda p: p.bet == smallest_all_in_bet_size,
                           all_ins)
                self._debug("Handling all-in of %d: %s " % \
                                (smallest_all_in_bet_size,
                                 " ".join([str(p) for p in \
                                               smallest_all_in_players])))
                # Sanity check
                if smallest_all_in_bet_size == 0:
                    raise PokerGameStateException("Smallest all-in bet is zero")
                # Subtract this all-in bet from all bets and put
                # into current pot
                self.pot.pull_bets(maximum_pull = smallest_all_in_bet_size)
                if len(self.players_with_bets()) > 0:
                    # If we only have one one player left we go
                    # ahead and create another pot which that player will
                    # automatically win.
                    self.pot.new_side_pot()
        self._debug("Sweep into pot complete")
        return self.pot

    def max_bet(self):
        """Return the larger total bet by any player."""
        return max([player.bet for player in self.table.get_seated_players()])

    def players_with_bets(self):
        """Return an array of players with non-zero bets."""
        return filter(lambda p: (p is not None) and (p.bet > 0),
                      self.table.get_seated_players())

    def _message(self, msg):
        """Handle a message"""
        if self.message_handler is not None:
            self.message_handler.message(msg)

    def _debug(self, msg):
        """Handle a debug message"""
        if self.message_handler is not None:
            self.message_handler.debug(msg)

######################################################################
class Structure(object):
    """Structure for a poker game.

    This is a set of read-only state regarding betting structure, namely
    limit, pot limit or no-limit, ante amount, blinds and minimum bet
    sizes for each round."""

    LIMIT = 0x00
    POT_LIMIT = 0x01
    NO_LIMIT = 0x02

    def __init__(self,
                 type,
                 ante,
                 blinds,
                 bet_sizes=None):
        """Create a betting structure for the game.

        type should one of TYPE_LIMT, TYPE_POT_LIMIT, TYPE_NO_LIMIT.

        ante should be the size of the ante each player pays per round.

        blind should be an array of blinds, from small to large.

        bet_sizes should be an array of the bet size for each round of betting.
        Or None if minimum bet is set by the big blind.
        """
        # TODO: Sanity check arguments
        self.type = type
        self.ante = ante
        self.blinds = blinds
        if bet_sizes is None:
            bet_sizes = max(blinds)
        self.bet_sizes = bet_sizes

    def is_limit(self):
        """Return True if this is a limit structure"""
        return self.type == self.LIMIT

    def is_pot_limit(self):
        """Return True if this is a pot limit structure"""
        return self.type == self.POT_LIMIT

    def is_no_limit(self):
        """Return True if this is a no limit structure"""
        return self.type == self.NO_LIMIT

    def get_ante(self):
        """Return the amount of the ante"""
        return self.ante

    def get_blinds(self):
        """Return an array of blinds from smallest to largest.

        Returns None if there are no blinds."""
        return self.blinds

    def get_minimum_bet(self, betting_round):
        """Return the minimum bet for the given betting round"""
        if isinstance(self.bet_sizes, list):
            return self.bet_sizes[betting_round]
        else:
            # One minimum for all rounds
            return self.bet_sizes

    def validate_bet(self, action, game_state):
        """Make sure bet represented by given action is legal.

        Raises InvalidAtionException if not legal."""
        # XXX This is assuming limit.
        # XXX This is ignoring a double bet allowed if pair showing
        bet_size = self.bet_sizes[game_state.betting_round]
        if action.amount != bet_size:
            raise InvalidActionException("Invalid bet size: %d != %d" % \
                                             (action.amount, bet_size))
