"""Base class for all pyPoker Hands."""

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

class TooManyCardsException(PokerException):
    """Tried to add more cards to a Hand then it should hold."""
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

    @classmethod
    def fromString(cls, string):
	return cls(Cards().fromString(string))

    @classmethod
    def getMaxCards(cls):
	return cls.maxCards

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
 
