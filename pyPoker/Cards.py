######################################################################
#
# Cards.py
#
# Classes for representing a playing cards.
#
# vwelch@ncsa.uiuc.edu
# $Id$
#
######################################################################

from PokerException import PokerException
from Utils import assertInstance

######################################################################

class BadSuitException(PokerException):
    """Provided suit was invalid."""
    pass

class BadRankException(PokerException):
    """Provided rank was invalid."""
    pass

class BadCardValueException(PokerException):
    """The value for a Card creation was invalid."""
    pass

class NotEnoughCardsException(PokerException):
    """Tried to get more cards than are left."""
    pass

######################################################################


class Suit:
    CLUB = 1
    CLUBS = 1
    DIAMOND = 2
    DIAMONDS = 2
    HEART = 3
    HEARTS = 3
    SPADE = 4
    SPADES = 4

    suits = range(CLUBS, SPADES + 1)

    suitsShortString = { CLUBS:"C", DIAMONDS:"D", HEARTS:"H", SPADES:"S" }

    suitsLongString =  { CLUBS:"clubs", DIAMONDS:"diamonds",
			 HEARTS:"hearts", SPADES:"spades" }

    def __init__(self, value):
	if isinstance(value, Suit):
	    self.value = value.value
	else:
	    if Suit.suits.count(value) == 0:
		raise BadSuitException("Invalud value %d" % value)
	    self.value = value

    def fromString(string):
	char = string.upper()
	for key in Suit.suitsShortString.keys():
	    if Suit.suitsShortString[key] == char:
		break
	else:
	    raise BadRankException("Bad suit \"%s\"" % char)
	return Suit(key)

    fromString = staticmethod(fromString)

    def random():
	import random
	value = random.randint(Suit.CLUBS, Suit.SPADES)
	return Suit(value)

    random = staticmethod(random)

    def __str__(self):
	return self.suitsShortString[self.value]

    def str(self):
	return self.__str()

    def shortString(self):
	return self.suitsShortString[self.value]

    def longString(self):
	return self.suitsLongString[self.value]

    def __cmp__(self, other):
	# Optimize for comparison to other Suit object
	try:
	    return cmp(self.value, other.value)
	except:
	    pass
	# Must be int
	return cmp(self.value, other)

######################################################################


class Rank:
    ACE_LOW = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    
    ranks = range(2, ACE + 1)

    ranksShortString = { ACE:"A", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6",
			 7:"7", 8:"8", 9:"9", 10:"T", JACK:"J", QUEEN:"Q",
			 KING:"K" }

    ranksLongString = { ACE:"ace", 2:"two", 3:"three", 4:"four", 5:"five",
			6:"six", 7:"seven", 8:"eight", 9:"nine", 10:"ten",
			JACK:"jack", QUEEN:"queen", KING:"king" }

    ranksPluralString = { ACE:"aces", 2:"twos", 3:"threes", 4:"fours",
			  5:"fives", 6:"sixes", 7:"sevens", 8:"eights",
			  9:"nines", 10:"tens", JACK:"jacks",
			  QUEEN:"queens", KING:"kings" }

    # Should aces be considered as low
    acesLow = False

    def __init__(self, value):
	if isinstance(value, Rank):
	    self.value = value.value
	else:
	    if Rank.ranks.count(value) == 0:
		raise BadRankException("Invalid value %d" % value)
	    self.value = value

    def fromString(string):
	char = string.upper()
	for key in Rank.ranksShortString.keys():
	    if Rank.ranksShortString[key] == char:
		break
	else:
	    raise BadRankException("Bad rank \"%s\"" % char)
	return Rank(key)

    fromString = staticmethod(fromString)

    def random():
	import random
	value = random.randint(2, Rank.ACE)
	return Rank(value)

    random = staticmethod(random)

    def __str__(self):
	return Rank.ranksShortString[self.value]

    def str(self):
	return self.__str()

    def shortString(self):
	return self.ranksShortString[self.value]

    def longString(self):
	return self.ranksLongString[self.value]

    def pluralString(self):
	return self.ranksPluralString[self.value]

    def acesAreLow(cls):
	cls.acesLow = True

    acesAreLow = classmethod(acesAreLow)

    def acesAreHigh(cls):
	cls.acesLow = False

    acesAreHigh = classmethod(acesAreHigh)

    def __cmp__(self, other):
	# Optimize for comparison with other Rank object
	try:
	    otherRank = other.value
	except:
	    # Must be int
	    otherRank = other
	selfValue = self.value
	if (self.acesLow):
	    if (selfValue == Rank.ACE):
		selfValue = Rank.ACE_LOW
	    if (otherRank == Rank.ACE):
		otherRank = Rank.ACE_LOW
	return cmp(selfValue, otherRank)

    def __add__(self, value):
	return Rank(self.value + value)

######################################################################

class Card:
    def __init__(self, tuple=None):
	"""Create a Card. Single argument can have following values:

	None - create uninitialized card.
	(rank,suit) - tuple of rank and suit, e.g. (10, CLUBS), (ACE, SPADES)
	"""
	if tuple:
	    rank, suit = tuple
	    self.rank = Rank(rank)
	    self.suit = Suit(suit)

    def fromString(string):
	if len(string) != 2:
	    raise BadCardValueException("Bad card string (%s) - wrong length (!=2)" % desc)
	string = string.upper()
	c = Card()
	c.rank = Rank.fromString(string[0])
	c.suit = Suit.fromString(string[1])
	return c

    fromString = staticmethod(fromString)

    def __str__(self):
	return str(self.rank) + str(self.suit)

    def shortString(self):
	return self.__str__()

    def longString(self):
	return self.rank.longString() + " of " + self.suit.longString()

    def __cmp__(self, other):
	# Ignore suit, optimize for comparison with other Card object
	try:
	    return cmp(self.rank, other.rank)
	except:
	    # other must be int
	    return cmp(self.rank, other)

    def eq(self, other):
	"""Return True of cards are identicial, including suit."""
	assertInstance(other, Card)
	return (self.suit == other.suit) and (self.rank == other.rank)

    def copy(self):
	"""Return a copy of myself."""
	import copy
	return copy.copy(self)

######################################################################
#
# Cards Object
#

class Cards(list):
    def __init__(self, cards=None):
	"""Create an array of cards.
	If cards is not None, it should be an array of the initial cards to be
	contained in the Cards object."""
	if cards:
	    self.addCards(cards)

    def addCard(self, card):
	"""Add given card to array."""
	self.append(card)

    def addCardFromString(self, string):
	"""Add a card described by string."""
	self.append(Card.fromString(string))

    def addCards(self, cards):
	"""Adds array of cards."""
	self.extend(cards)

    def addCardsFromString(self, string):
	"""Adds card from sting (e.g '4H 7C 9D')."""
	self.extend(Cards.fromString(string))

    def fromString(cls, string):
	"""Create an object from string, which is a whitespace-separated
	list of cards (e.g. '4H 7C 9D')."""
	return cls.fromStrings(string.split())

    fromString = classmethod(fromString)

    def fromStrings(cls, strings):
	"""Create an object from an array of strings, eacho of which
	description of a card (e.g. ['4H','7C','9D'])."""
	return cls([Card().fromString(s) for s in strings])

    fromStrings = classmethod(fromStrings)

    def sort(self):
	"""Sort cards so they are high to low."""
	list.sort(self)
	list.reverse(self)

    def str(self):
	return self.__str__()

    def __str__(self):
	string = ''
	for card in self:
	    string = string + str(card) + ' '
	return string.strip()

    def copy(self):
	import copy
	return copy.copy(self)

    def combinations(self, n):
	"""Generator function returning all combinations of n cards."""
	assertInstance(n, int)
	if n > len(self):
	    raise NotEnoughCardsException("Cannot generate %d cards from only %d cards" % (n, len(self)))
	if n == 0:
	    yield Cards()
	elif n == 1:
	    for card in self:
		c = Cards()
		c.append(card)
		yield c
	elif n == len(self):
	    # Optimization
	    yield self.copy()
	else:
	    for index in xrange(len(self) - n + 1):
		remainder = self[index+1:]
		for subComb in remainder.combinations(n-1):
		    subComb.append(self[index])
		    yield subComb
 
    def sameSuit(self):
	"""Are all cards the same suit?"""
	for index in range(len(self) - 1):
	    if self[index].suit != self[index+1].suit:
		return False
	return True

    def consecutivelyDescending(self):
	"""Are cards consecutively descending? Used for straight testing.
	If there is only one card in the array, returns True."""
	try:
	    for index in range(len(self)-1):
		if (self[index].rank != (self[index+1].rank + 1)):
		    return False
	except BadRankException:
	    # When out of bounds, which means we had an ACE in card past first
	    # so we cannot be consectively descending
	    return False
	return True

    def __getslice__(self, start, stop):
	"""Allow slices to return a Cards object instead of a list object."""
	slice = super(Cards, self).__getslice__(start, stop)
	cards = Cards()
	cards.extend(slice)
	return cards
