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


class Suit(int):
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
	# At this point self has already been set
	if Suit.suits.count(self) == 0:
	    raise BadSuitException("Invalud value %d" % self)

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
	return self.suitsShortString[self]

    def str(self):
	return self.__str()

    def shortString(self):
	return self.suitsShortString[self]

    def longString(self):
	return self.suitsLongString[self]


######################################################################


class Rank(int):
    UNDEFINED = 0
    # Equivalent to ACE, but makes it easier to evaluate low hand
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
    
    ranks = range(ACE_LOW, ACE + 1)

    ranksShortString = { ACE:"A", ACE_LOW:"A",
                         2:"2", 3:"3", 4:"4", 5:"5", 6:"6",
			 7:"7", 8:"8", 9:"9", 10:"T", JACK:"J", QUEEN:"Q",
			 KING:"K" }

    ranksLongString = { ACE:"ace", ACE_LOW:"A",
                        2:"two", 3:"three", 4:"four", 5:"five",
			6:"six", 7:"seven", 8:"eight", 9:"nine", 10:"ten",
			JACK:"jack", QUEEN:"queen", KING:"king" }

    ranksPluralString = { ACE:"aces", ACE_LOW:"aces",
                          2:"twos", 3:"threes", 4:"fours",
			  5:"fives", 6:"sixes", 7:"sevens", 8:"eights",
			  9:"nines", 10:"tens", JACK:"jacks",
			  QUEEN:"queens", KING:"kings" }


    def __init__(self, value):
	# At this point self has already been set
	if Rank.ranks.count(self) == 0:
	    raise BadRankException("Invalid rank value %d" % value)

    def fromString(string):
	char = string.upper()
        # Special case "A" to it doesn't become ACE_LOW
        if char == "A":
            return Rank(Rank.ACE)
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
	return Rank.ranksShortString[self]

    def str(self):
	return self.__str()

    def shortString(self):
	return self.ranksShortString[self]

    def longString(self):
	return self.ranksLongString[self]

    def pluralString(self):
	return self.ranksPluralString[self]

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

    def makeAcesLow(self):
        """Make any ace low."""
        if self.rank == Rank.ACE:
            self.rank = Rank(Rank.ACE_LOW)

    def makeAcesHigh(self):
        """Make any ace high."""
        if self.rank == Rank.ACE_LOW:
            self.rank = Rank(Rank.ACE)

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
	return cls([Card.fromString(s) for s in strings])

    fromStrings = classmethod(fromStrings)

    def sort(self):
	"""Sort cards so they are high to low."""
	list.sort(self)
	list.reverse(self)

    def makeAcesLow(self):
        """Make aces low."""
        for card in self:
            card.makeAcesLow()

    def makeAcesHigh(self):
        """Make aces high."""
        for card in self:
            card.makeAcesHigh()

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
	from Utils import combinations
	return combinations(self, n)
 
    def sameSuit(self):
	"""Are all cards the same suit?"""
	for index in range(len(self) - 1):
	    if self[index].suit != self[index+1].suit:
		return False
	return True

    def suitedCards(self, suit):
	"""Return cards of given suit."""
	cards = Cards()
	for card in self:
	    if card.suit == suit:
		cards.append(card)
	return cards

    def rankCount(self, rank):
	"""Return number of cards of given rank."""
	count = 0
	for card in self:
	    if card.rank == rank:
		count += 1
	return count

    def countRanks(self):
	"""Return an array containing a count of how often each rank appears."""
	count = [0] * (Rank.ACE + 1)
	for rank in Rank.ranks:
	    count[rank] = self.rankCount(rank)
	return count

    def removeRank(self, rank):
	"""Remove all cards matching rank."""
	index = 0
	while index < len(self):
	    if self[index].rank == rank:
		del self[index]
		continue
	    index += 1

    def suitCount(self, suit):
	"""Return number of cards of given suit."""
	count = 0
	for card in self:
	    if card.suit == suit:
		count += 1
	return count

    def __getslice__(self, start, stop):
	"""Allow slices to return a Cards object instead of a list object."""
	slice = super(Cards, self).__getslice__(start, stop)
	cards = Cards()
	cards.extend(slice)
	return cards

    def haveSuitedAce(self):
	"""Return True if we have an Ace and another card of the same suit."""
	# Quick optimization, if we have no ace, then we're done
	if self.rankCount(Rank.ACE) == 0:
	    return False
	for suit in Suit.suits:
	    suitedCards = self.suitedCards(suit)
	    if ((len(suitedCards) > 1) and
		suitedCards.rankCount(Rank.ACE)):
		return True
	return False

    def bigCardCount(self):
	"""Return number of cards that are a Ten, Jack, Queen, King or Ace."""
	count = 0
	for card in self:
	    if ((card.rank == Rank.ACE) or
		(card.rank > Rank.NINE)):
		count += 1
	return count

    def babyCount(self):
	"""Return number of cards that are babies (Ace through Five)."""
	count = 0
	for card in self:
	    if card.rank < Rank.SIX:
		count += 1
	return count

    
