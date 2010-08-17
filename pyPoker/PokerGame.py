"""Class for simulating poker games."""

from PokerException import PokerException
from Hand import Hand, CommunityCardHand, FiveCardStudHand, SevenCardStudHand, OmahaHand
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

    # For each hand, number of wins high
    highWins = []

    # For each hand, number of wins low
    lowWins = []

    # For each hand, number of scoops (wins both ways)
    scoops = []

    # What game number are we playing
    gameNum = 0

    # Hands from last game simulated
    lastGameHands = None

    # Board from last game simulated
    lastGameBoard = None

    # High winners for last game simulated
    lastGameHighWinners = None

    # High rank for last game simulated
    lastGameHighRank = None

    # Low winners for last game simulated
    lastGameLowWinners = None

    # Low rank for last game simulated
    lastGameLowRank = None

    # Scoopers for last game simulated
    lastGameScoopers = None

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
	self.highWins = []
	self.lowWins = []
	self.scoops = []
	if hands:
	    self.addHands(hands)

    def resetStats(self):
	numHands  =  max(len(self.hands), self.numHands)
	if self.highHandsWin:
	    self.highWins = [ 0 ] * numHands
	if self.lowHandsWin:
	    self.lowWins = [ 0 ] * numHands
	if self.lowHandsWin and self.highHandsWin:
	    self.scoops = [ 0 ] * numHands
	self.gameNum = 0

    def __checkStatArrays(self):
	"""Make sure all the statistic arrays are long enough.
	In case a hand was added since we last simualted a game."""
	if len(self.highWins) < len(self.hands):
	    self.highWins.extend([ 0 ] * (len(self.hands)-len(self.highWins)))
	if len(self.lowWins) < len(self.hands):
	    self.lowWins.extend([ 0 ] * (len(self.hands)-len(self.lowWins)))
	if len(self.scoops) < len(self.hands):
	    self.scoops.extend([ 0 ] * (len(self.hands)-len(self.scoops)))

    @classmethod
    def getHandClass(cls):
	return cls.handClass

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

    def getHighWins(self):
	"""Return an array with how many times each hand won high."""
	if not self.highHandsWin:
	    return None
	return self.highWins

    def getLowWins(self):
	"""Return an array with how many times each hand won low."""
	if not self.lowHandsWin:
	    return None
	return self.lowWins

    def getWins(self):
	"""Return total wins by each hand (high or low)."""
	if not self.lowHandsWin:
	    return self.highWins
	if not self.highHandsWin:
	    return self.lowWins
	wins = []
	for hand in self.highWins:
	    wins = self.highWins[hand] + self.lowWins[hand]
	return wins

    def getScoops(self):
	"""Return an array with how many times each hand won both ways."""
	if not (self.highHandsWin and self.lowHandsWin):
	    return None
	return self.scoops

    def simulateGames(self, numGames = 100, callback=None, callbackArg=None,
		      resetStats = True):
	"""Simulate a bunch of games with starting hands. Returns
	a array with number of wins for each hand."""
	assertInstance(numGames, int)
	if self.getNumHands() == 0:
	    raise PokerGameStateException("Zero hands defined.")
	if resetStats:
	    self.resetStats()
	while self.gameNum < numGames:
	    self.simulateGame()
	    if callback is not None:
		if callbackArg:
		    callback(self, callbackArg)
		else:
		    callback(self)

    def simulateGame(self):
	self.__checkStatArrays()
	self.gameNum += 1
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
	    self.lastGameBoard = board
	self.lastGameHands = hands
	# Find winning hands
	if self.highHandsWin:
	    (bestHighRank, highWinners) = self._findHighHands(hands, board)
	    self.lastGameHighWinners = highWinners
	    self.lastGameHighRank = bestHighRank
	    for winner in highWinners:
		self.highWins[winner] += 1
	if self.lowHandsWin is True:
	    (bestLowRank, lowWinners) = self._findLowHands(hands, board)
	    self.lastGameLowWinners = lowWinners
	    self.lastGameLowRank = bestLowRank
	    for winner in lowWinners:
		self.lowWins[winner] += 1
	if self.lowHandsWin and self.highHandsWin:
	    self.lastGameScooper = self._findScooper(lowWinners, highWinners)
	    if self.lastGameScooper is not None:
		self.scoops[self.lastGameScooper] += 1

    def _findHighHands(self, hands, board):
	highWinners = [ 0 ]
	bestHighRank = self.highHandRanker.rankHand(hands[0])
	for index in range(1,len(hands)):
	    rank = self.highHandRanker.rankHand(hands[index])
	    if rank == bestHighRank:
		highWinners.append(index)
	    elif rank > bestHighRank:
		highWinners = [index]
		bestHighRank = rank
	return (bestHighRank, highWinners)

    def _findLowHands(self, hands, board):
	if self.lowHandEightOrBetter and (board is not None):
	    # See if low is possible given board
	    if board.eightLowPossible() is False:
		# Nope, don't bother checking for low hands
		return (None, [])
	bestLowRank = None
	lowWinners = []
	for index in range(len(hands)):
	    hand = hands[index]
	    if (self.lowHandEightOrBetter and
		(hand.eightLowPossible() is False)):
		# Hand cannot qualify for low, don't bother checking
		continue
	    rank = self.lowHandRanker.rankHand(hand)
	    if (self.lowHandEightOrBetter and
		(not rank.isEightOrBetterLow())):
		# Hand did not qualify for low
		continue
	    if ((bestLowRank is None) or
		(rank < bestLowRank)):
		lowWinners = [index]
		bestLowRank = rank
	    elif rank == bestLowRank:
		lowWinners.append(index)
	return (bestLowRank, lowWinners)

    def _findScooper(self, lowWinners, highWinners):
	"""Was there one winner of the whole pot?"""
	if ((len(lowWinners) == 1) and
	    (len(highWinners) == 1) and
	    (lowWinners[0] == highWinners[0])):
	    return lowWinners[0];
	return None

    def lastGameToString(self):
	import string
	s=""
	if self.hasBoard():
	    s += "Board: " + str(self.lastGameBoard) + " "
	if self.highHandsWin:
	    s += "High: %s " % self.lastGameHighRank
	    s += "("
	    s += ",".join(["%d:%s" % (hand + 1, self.lastGameHands[hand])
			   for hand in self.lastGameHighWinners])
	    s += ") "
	if self.lowHandsWin and len(self.lastGameLowWinners):
	    s += "Low: %s " % self.lastGameLowRank
	    s += "("
	    s += ",".join(["%d:%s" % (hand + 1, self.lastGameHands[hand])
			   for hand in self.lastGameLowWinners])
	    s += ") "
	if self.lowHandsWin and self.highHandsWin:
	    if self.lastGameScooper is not None:
		s += "(Hand %d scoops)" % (self.lastGameScooper + 1)
	s.strip()
	return s

    def statsToString(self):
	s = ""
	for hand in range(self.getNumHands()):
	    s += "%2d:" % (hand + 1)
	    if hand >= len(self.hands):
		handStr = "XX " * self.handClass.getMaxCards()
		s += handStr
	    else:
		s += str(self.hands[hand]) + " "
	    if self.highHandsWin:
		wins = self.highWins[hand]
		s += "High wins %4d (%3.0f%%)" % (
		    wins,
		    100.0 * wins / self.gameNum)
	    if self.lowHandsWin:
		wins = self.lowWins[hand]
		s += " Low wins %4d (%3.0f%%)" % (
		    wins,
		    100.0 * wins / self.gameNum)
	    if self.highHandsWin and self.lowHandsWin:
		s += " Scoops: %d" % self.scoops[hand]
	    s += "\n"
	return s

class CommunityCardPokerGame(PokerGame):
    handClass = CommunityCardHand
    gameName = "Community Card Poker"

    def __init__(self, numHands = 0, hands=None, board=None):
	PokerGame.__init__(self, numHands=numHands, hands=None)
	if board is None:
	    board = self.handClass.boardClass()
	self.setBoard(board)

class FiveCardStudGame(PokerGame):
    handClass = FiveCardStudHand
    gameName = "Five-card Stud"

class FiveCardStudHiLoGame(FiveCardStudGame):
    lowHandRankerClass = LowRanker
    gameName = "Five-card Stud Hi/Lo"

class SevenCardStudGame(PokerGame):
    handClass = SevenCardStudHand
    gameName = "Seven-card Stud"

class SevenCardStudHiLoGame(SevenCardStudGame):
    lowHandRankerClass = LowRanker
    gameName = "Seven-card Stud Hi/Lo"

class OmahaGame(CommunityCardPokerGame):
    handClass = OmahaHand
    gameName = "Omaha"

class OmahaHiLoGame(OmahaGame):
    lowHandRankerClass = LowRanker
    lowHandEightOrBetter = True
    gameName = "Omaha Hi/Lo 8-or-better"

