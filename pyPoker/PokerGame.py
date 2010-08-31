"""Class for simulating poker games."""

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


                
        
            
