######################################################################
#
# PokerGame.py
#
# Class for simulating poker games.
#
# vwelch@ncsa.uiuc.edu
# $Id$
#
######################################################################

from PokerException import PokerException
from Hand import Hand, Hands, CommunityCardHand, HoldEmHand, FiveCardStudHand, OmahaHand
from Cards import Cards
from Deck import Deck
from Utils import assertInstance
from PokerRank import PokerRank

######################################################################
#
# Exceptions
#

class PokerGameStateException(PokerException):
    """Error in state for game simulation."""
    pass

######################################################################
#
# Temporary hack
#

class HandGenerator:
    pass

######################################################################
#
# PokerGame
#

class PokerGame:
    # Type of hand used in this game, should be redefined in subclasses
    handClass = Hand

    # Support for board here, but don't allow setting in this class
    board = None

    # Winning hands: high, low or both?
    highHandsWin = True
    lowHandsWin = False

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
	self.deck = Deck()
	self.numHands = numHands
	self.hands = Hands()
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

    def getHandClass(cls):
	return cls.handClass

    getHandClass = classmethod(getHandClass)

    def addHands(self, hands):
	if hands is None:
	    return
	if isinstance(hands, Hand) or isinstance(hands, HandGenerator):
	    hands = [ hands ]
	for hand in hands:
	    if hand is None:
		self.hands.addHand(self.handClass())
	    elif isinstance(hand, HandGenerator):
		self.hands.addHand(hand)
	    else:
		self.hands.addHand(hand)
		self.deck.removeCards(hand)
	# If we already have statistics, then extend win arrays to match
	# length of new array of hands
	if self.gameNum > 0:
	    if self.highHandsWin:
		self.highWins.extend([ 0 ] * len(hands))
	    if self.lowHandsWin:
		self.lowWins.extend([ 0 ] * len(hands))
	    if self.highHandsWin and self.lowHandsWin:
		self.scoops.extend([ 0 ] * len(hands))
				     
    def addHand(self, hand):
	assertInstance(hand, [Hand, HandGenerator])
	self.addHands(hand)

    def getNumHands(self):
	return max(self.numHands, len(self.hands))

    def getHands(self):
	return self.hands

    def hasBoard(self):
	return (self.handClass.boardClass != None)

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
	if resetStats or self.gameNum == 0:
	    self.resetStats()
	while self.gameNum < numGames:
	    self.simulateGame()
	    if callback is not None:
		if callbackArg:
		    callback(self, callbackArg)
		else:
		    callback(self)

    def simulateGame(self):
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
	if self.highHandsWin is True:
	    (bestHighRank, highWinners) = self._findHighHands(hands)
	    self.lastGameHighWinners = highWinners
	    self.lastGameHighRank = bestHighRank
	    for winner in highWinners:
		self.highWins[winner] += 1
	if self.lowHandsWin is True:
	    (bestLowRank, lowWinners) = self._findLowHands(hands)
	    self.lastGameLowWinners = lowWinners
	    self.lastGameLowRank = bestLowRank
	    for winner in lowWinners:
		self.lowWins[winner] += 1
	if self.lowHandsWin and self.highHandsWin:
	    self.lastGameScoopers = self._findScoopers(lowWinners, highWinners)

    def _findHighHands(self, hands):
	highWinners = [ 0 ]
	bestHighRank = PokerRank(hands[0])
	for index in range(1,len(hands)):
	    rank = PokerRank(hands[index])
	    if rank == bestHighRank:
		highWinners.append(index)
	    elif rank > bestHighRank:
		highWinners = [index]
		bestHighRank = rank
	return (bestHighRank, highWinners)

    def _findLowHands(self, hands):
	lowWinners = [ 0 ]
	bestLowRank = PokerRank.lowRank(hands[0])
	for index in range(1,len(hands)):
	    rank = PokerRank.lowRank(hands[index])
	    if rank == bestLowRank:
		lowWinners.append(index)
	    elif rank < bestLowRank:
		lowWinners = [index]
		bestLowRank = rank
	if self.lowHandEightOrBetter and not bestLowRank.isEightOrBetterLow():
	    # Winner did not qualify for low
	    return (None, [])
	return (bestLowRank, lowWinners)

    def _findScoopers(self, lowWinners, highWinners):
	scoopers = []
	for winner in lowWinners:
	    if highWinners.count(winner):
		self.scoops[winner] += 1
		scoopers.append(winner)
	return scoopers

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
	    if len(self.lastGameScoopers):
		s += " Scoopers: "
		for scooper in self.lastGameScoopers:
		    s += str(scooper + 1) + " "
	s.strip()
	return s
	    

class CommunityCardPokerGame(PokerGame):
    handClass = CommunityCardHand

    def __init__(self, numHands = 0, hands=None, board=None):
	PokerGame.__init__(self, numHands=numHands, hands=None)
	if board is None:
	    board = self.handClass.boardClass()
	self.setBoard(board)

class HoldEmGame(CommunityCardPokerGame):
    handClass = HoldEmHand

class FiveCardStudHiLoGame(PokerGame):
    handClass = FiveCardStudHand
    highHandsWin = True
    lowHandsWin = True

class OmahaGame(CommunityCardPokerGame):
    handClass = OmahaHand

class OmahaHiLoGame(OmahaGame):
    highHandsWin = True
    lowHandsWin = True
    lowHandEightOrBetter = True

