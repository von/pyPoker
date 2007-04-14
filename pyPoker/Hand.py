######################################################################
#
# Hand.py
#
# Base class for all pyPoker Hands.
#
# vwelch@ncsa.uiuc.edu
# $Id$
#
######################################################################

from PokerException import PokerException
from Cards import Cards, Card, Rank, Suit, BadRankException, NotEnoughCardsException
from Utils import assertInstance
    
######################################################################
#
# Exceptions
#

class IncompleteHandException(PokerException):
    """Tried to get the rank of a hand that wasn't complete."""
    pass

class InvalidHandTypeException(PokerException):
    """Invalid type of hand passed as argument."""
    pass

class HandHasNoBoardException(PokerException):
    """Tried to set or get a board for a hand that doesn't support it."""
    pass

######################################################################
#
# Hand Class
#

class Hand(Cards):

    # These functions have support for community cards (aka a "board")
    # to splify coding with regards to community hands. However, this
    # class doesn't support setting it.
    board = None
    boardClass = None

    # Maximum number of cards in hand
    maxCards = 5

    def __init__(self, cards = None, maxCards=None):
	"""Create a new hand. Arguments:

	cards - should incate would cards the hand should initially contain.
	This can be either:
	    A Cards array
	    A string suitable for passing to the Cards creation method.

	maxCards - maximum number of cards hands should contain. If more
	cards than this are added, an exception will be raised. If None
	then no maximum is enforced.
	"""
	if cards:
	    self.addCards(cards)

    def fromString(cls, string):
	return cls(Cards().fromString(string))

    fromString = classmethod(fromString)

    def getMaxCards(cls):
	return cls.maxCards

    getMaxCards = classmethod(getMaxCards)

    def numCards(self):
	if self.board:
	    return len(self) + len(self.board)
	else:
	    return len(self)

    def append(self, card):
	"""Append while checking to be sure maxCards is not exceeded."""
	if self.maxCards and (len(self) == self.maxCards):
	    raise TooManyCardsException()
	assertInstance(card, Card)
	Cards.append(self, card)

    def extend(self, cards):
	"""Extend while checking to be sure maxCards is not exceeded."""
	if self.maxCards:
	    if len(self) + len(cards) > self.maxCards:
		raise TooManyCardsException()
	Cards.extend(self, cards)

    def __str__(self):
	string = Cards.__str__(self)
	for card in range(self.maxCards - len(self)):
	    string += " xx"
	return string.strip()

    def copy(self):
	"""Return a copy of this Hand."""
	import copy
	return copy.copy(self)

    def hands(self):
	"""Return all sets of cards that can be constructed from hand."""
	cards = Cards(self)
	if self.board:
	    cards.extend(self.board)
	yield cards

    def combinations(self, n):
	"""Generator function return all combinations of n cards (including
	community cards)."""
	assertInstance(n, int)
	cards = Cards(self)
	if self.board:
	    cards.extend(self.board)
	return Cards.combinations(cards, n)

    def eq(self, otherHand):
	"""Are two hands identical (including suits)?"""
	if len(self) != len(otherHand):
	    return False
	for index in range(len(self)):
	    if self[index].eq(otherHand[index]):
		return False
	return True

    def countEightOrLower(self):
	"""Return number of cards eight or lower (including aces), but discounting duplicated ranks."""
	lowRanks = set()
	for card in self:
	    if ((card.rank <= Rank.EIGHT) or
		(card.rank == Rank.ACE)):
		lowRanks.add(card.rank)
	return len(lowRanks)

######################################################################
#
# Stud Hand (for future expansion)
#

class StudHand(Hand):
    """A Stud hand."""
    upCards = []

    def isUpCard(self, index):
	"""Return true if index represents the position of a up card."""
	return (self.upCards.count(index) != 0)

    def isDownCard(self, index):
	"""Return true if index represents the position of a down card."""
	return (self.upCards.count(index) == 0)

    def getDownCards(self):
	cards = Cards()
	for card in range(len(self)):
	    if self.isDownCard(card):
		cards.append(self[card])
	return cards

    def getUpCards(self):
	cards = Cards()
	for card in range(len(self)):
	    if self.isUpCard(card):
		cards.append(self[card])
	return cards
	
    def str(self, showDown=True, indicateDown=True):
	string = ""
	for index in range(len(self)):
	    if self.isDownCard(index):
		if not showDown:
		    string += "** "
		elif indicateDown:
		    string += "(" + str(self[index]) + ") "
		else:
		    string += (self[index]) + " "
	    else:
		string += str(self[index]) + " "
	for card in range(self.maxCards - len(self)):
	    string += "xx "
	return string.strip()
	    
class FiveCardStudHand(StudHand):
    """A five card stud hand."""
    upCards = [1,2,3,4]
    maxCards = 5

class SevenCardStudHand(StudHand):
    """A five card stud hand."""
    upCards = [2,3,4,5]
    maxCards = 7

######################################################################
#
# Community Hand and Board classes
#

class Board(Hand):
    """A hand representing a set of community cards."""

    def eightLowPossible(self):
	"""Return true if this board can produce a eight or better low."""
	return (self.countEightOrLower() >= 3)

    def paired(self):
	"""Return true if board is paired."""
	for index in range(len(self) - 1):
	    for subindex in range(index + 1, len(self)):
		if self[index].rank == self[subindex].rank:
		    return True
	return False

class FiveCardBoard(Board):
    """A hand representing a five-card board."""
    pass

class CommunityCardHand(Hand):
    """A hand with a set of community cards (aka a 'board')."""

    boardClass = Board

    def __init__(self, cards = None, board=None):
	"""Create a new hand. Arguments:

	cards - should be an array of Cards that the hand should contain.
	Otherwise it will have no cards.

	board - set of community cards associated with this hand.
	"""
	Hand.__init__(self, cards)
	if board:
	    self.setBoard(board)

    def getBoard(self):
	"""Return board for given hand."""
	return self.board

    def setBoard(self, cards):
	"""Set board for hand. cards should be a Board object."""
	assertInstance(cards, Cards)
	self.board = cards

    def getHoleCards(self):
	"""Return the hole (non-community) cards."""
	c = Cards()
	c.extend(self)
	return c
 
######################################################################
#
# Texas HoldEm
#


class HoldEmHand(CommunityCardHand):
    maxCards = 2
    boardClass = FiveCardBoard

    def __init__(self, cards = None, board = None):
	"""Create a Texas Hold'Em hand.
	cards should be none or an array of up to two cards.
	board should be a Board object."""
	CommunityCardHand.__init__(self, cards, board = board)

######################################################################
#
# Omaha
#

class OmahaHand(CommunityCardHand):
    maxCards = 4
    boardClass = FiveCardBoard

    def __init__(self, cards = None, board = None):
	"""Create a Omaha hand.
	cards should be None or an array of up to four cards.
	board should be a Board object."""
	CommunityCardHand.__init__(self, cards, board = board)

    def hands(self):
	"""Return all sets of cards that can be constructed from hand."""
	for hand in self.combinations(5):
	    yield hand

    def combinations(self, n):
	"""Generator function return all combinations of n cards (including
	community cards)."""
	assertInstance(n, int)
	holeCards = self.getHoleCards()
	if n <= 2:
	    for holeCombo in holeCards.combinations(n):
		yield holeCombo
	elif self.board:
	    for holeCombo in holeCards.combinations(2):
		for boardCombo in self.board.combinations(n-2):
		    combo = holeCombo.copy()
		    combo.extend(boardCombo)
		    yield combo
	else:
	    raise NotEnoughCardsException("Cannout generated hand of %d cards without board." % n)

    def eightLowPossible(self):
	"""Return true if this hand can have a eight or better low."""
	return (self.countEightOrLower() >= 2)

    def pointValue(self):
	"""Return the point value of the hand as defined by:
http://casinogambling.about.com/cs/poker/a/omahahilo_2.htm"""
	total = 0
	# Count pairs. A pair adds points equal to rank of card, 30 for aces.
	# Give half-credit for trips and none for quads
	for rank in Rank.ranks:
	    value = rank
	    if rank == Rank.ACE:
		value = 30
	    count = self.rankCount(rank)
	    if count == 2:
		total += value
	    elif count == 3:
		total += value/2
	# Count flushes. Two-flush with Ace gives 10 points, 4 points otherwise.
	# Half credit for three or four flush
	for suit in Suit.suits:
	    suitedCards = self.suitedCards(suit)
	    if suitedCards.rankCount(Rank.ACE) > 0:
		value = 10
	    else:
		value = 4
	    if len(suitedCards) == 2:
		total += value
	    elif len(suitedCards) > 2:
		total += value/2
	# Count straights
	# A two-straight with no or 1-card gap is two points
	for rank in range(Rank.SIX, Rank.ACE + 1):
	    for rank2 in range(rank - 2, rank):
		if self.rankCount(rank) and self.rankCount(rank2):
		    total += 2
	# High Cards. Unpaired Ace is 4 points, unpaired King in 2 points.
	if self.rankCount(Rank.ACE) == 1:
	    total += 4
	if self.rankCount(Rank.KING) == 1:
	    total += 2
	# Count low hands
	# A-2 is 20 points, A-3 is 15, 2-3 and A-4 is 10.
	# Other two babies are 5 points.
	acesLowState = Rank.getAcesLow()
	Rank.acesAreLow()
	for rank in range(Rank.ACE_LOW, Rank.FIVE):
	    for rank2 in range(rank + 1, Rank.SIX):
		if self.rankCount(rank) and self.rankCount(rank2):
		    if rank == Rank.ACE_LOW:
			if rank2 == Rank.TWO:
			    total += 20
			elif rank2 == Rank.THREE:
			    total += 15
			elif rank2 == Rank.FOUR:
			    total += 10
		    elif rank == Rank.TWO and rank2 == Rank.THREE:
			total += 10
		    else:
			total += 5
	Rank.setAcesLow(acesLowState)
	return total

    def openingHand(self):
	"""Is this an opening hand according to "Winning Omaha 8 Poker" by
Tenner and Krieger?"""
	# A2xx
	if self.rankCount(Rank.ACE):
	    if self.rankCount(Rank.TWO):
		# A3xx
		return True
	    if self.rankCount(Rank.THREE):
		if self.haveSuitedAce():
		    # As3xx	
		    return True
		if self.bigCardCount() == 3:
		    # A3XX
		    return True
	    if self.babyCount() > 2:
		# Abbx
		return True
	    if self.haveSuitedAce() and self.bigCardCount() > 2:
		# AsXXx
		return True
	if self.babyCount() == 4:
	    # bbbb
	    return True
	if self.bigCardCount() == 4:
	    # XXXX
	    return True
	return False

