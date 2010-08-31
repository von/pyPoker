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

######################################################################
#
# PokerGame
#

class PokerGame:
    # Type of hand used in this game, should be redefined in subclasses
    handClass = Hand

    # Type of Deck used in this game
    deckClass = Deck

    # Name of this game
    gameName = "Poker"

    # Support for board here, but don't allow setting in this class
    board = None

    # Class to use to determine rank for hi and/or low
    # If == None then no winner in that direction.
    highHandRankerClass = Ranker
    lowHandRankerClass = None

    # Ranker instances to use to determine hand ranks
    highHandRanker = None
    lowHandRanker = None

    # Low hand must be eight or berrer?
    lowHandEightOrBetter = False

    def __init__(self, numHands = 0, hands=None):
	assertInstance(numHands, int)
	self.deck = self.deckClass()
	if numHands and (numHands > self.getMaxHands()):
	    raise TooManyHandsException
	self.numHands = numHands
	self.hands = Hands()
	self.lowHandsWin = (self.lowHandRankerClass != None)
        if self.lowHandRankerClass:
            self.lowHandRanker = self.lowHandRankerClass()
	self.highHandsWin = (self.highHandRankerClass != None)
        if self.highHandRankerClass:
            self.highHandRanker = self.highHandRankerClass()
	if hands:
	    self.addHands(hands)
        
    @classmethod
    def getHandClass(cls):
	return cls.handClass

    @classmethod
    def highHandWins(cls):
        return cls.highHandRankerClass is not None

    @classmethod
    def lowHandWins(cls):
        return cls.lowHandRankerClass is not None

    def addHands(self, hands):
	if hands is None:
	    return
	if isinstance(hands, Hand) or isinstance(hands, HandGenerator):
	    hands = [ hands ]
	if len(self.hands) + len(hands) > self.getMaxHands():
	    raise TooManyHandsException
	for hand in hands:
	    if hand is None:
		self.hands.addHand(self.handClass())
	    else:
		self.hands.addHand(hand)
		self.deck.removeCards(hand)
				     
    def addHand(self, hand):
	assertInstance(hand, Hand)
	self.addHands(hand)

    def addHandGenerator(self, hg):
	assertInstance(hg, HandGenerator)
	self.hands.addHand(hg)

    @classmethod
    def getMaxHands(cls):
	cardsPerHand = cls.handClass.maxCards
	if cls.hasBoard():
	    boardCards = cls.handClass.boardClass.maxCards
	else:
	    boardCards = 0
	numCards = cls.deckClass.numCards - boardCards
	return int(numCards/cardsPerHand)
	
    def getNumHands(self):
	return max(self.numHands, len(self.hands))

    def getHands(self):
	return self.hands

    @classmethod
    def hasBoard(cls):
	return (cls.handClass.boardClass != None)

    def setBoard(self, board):
	if not self.hasBoard():
	    raise HandHasNoBoardException()
	if board:
	    assertInstance(board, Cards)
	    self.deck.removeCards(board)
	self.board = board

    def getBoard(self):
	if not self.hasBoard():
	    raise HandHasNoBoardException()
	return self.board

    def simulateGames(self, numGames = 100, callback=None, callbackArg=None,
		      stats=None):
	"""Simulate a bunch of games with starting hands. Returns
	a array with number of wins for each hand.

        Returns a Stats instance with the statistics from the games. If a
        stats instance is passed in, the same one, augmented, will be
        returned.

        callback should be a function that takes the form:
        callback(game, result, *callbackarg)
        """
	assertInstance(numGames, int)
	if self.getNumHands() == 0:
	    raise PokerGameStateException("Zero hands defined.")
        if stats is None:
            stats = Stats(number_of_hands = self.getNumHands())
	while numGames > 0:
	    result = self.simulateGame()
            stats.record_game(result)
	    if callback is not None:
                args = [self, result]
                if callbackArg is not None:
                    args.append(callbackArg)
                callback(*args)
            numGames -= 1
        return stats

    def simulateGame(self):
	# Make a copy of deck, hands and board
	deck = self.deck.copy()
	deck.shuffle()
	hands = Hands()
	for hand in self.hands:
	    if isinstance(hand, HandGenerator):
		hands.addHand(hand.generateHand(deck = deck))
	    else:
		hands.addHand(hand.copy())
	# If we have less than numHands, fill it out
	while len(hands) < self.numHands:
	    hands.addHand(self.handClass())
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
	if self.highHandsWin:
	    (high_winners, bestHighRank) = self.highHandRanker.bestHand(hands)
            result.high_winners = high_winners
            result.winning_high_rank = bestHighRank
	if self.lowHandsWin is True:
	    (low_winners, bestLowRank) = self.lowHandRanker.bestHand(hands)
            result.low_winners = low_winners
            result.winning_low_rank = bestLowRank
        return result

class CommunityCardPokerGame(PokerGame):
    handClass = CommunityCardHand
    gameName = "Community Card Poker"

    def __init__(self, numHands = 0, hands=None, board=None):
	PokerGame.__init__(self, numHands=numHands, hands=None)
	if board is None:
	    board = self.handClass.boardClass()
	self.setBoard(board)

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

    def get_high_winners(self):
        """Return an array with number of high wins by each hand"""
        return self.high_winners

    def get_low_winners(self):
        """Return an array with number of low wins by each hand"""
        return self.low_winners

    def get_scoops(self):
        """Return an array with number of scoops by each hand"""
        return self.scoops


                
        
            
