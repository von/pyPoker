######################################################################
#
# PokerRank.py
#
# Class for calculating and hold a Hand's rank.
#
# vwelch@ncsa.uiuc.edu
# $Id$
#
######################################################################

from PokerException import PokerException
from Cards import Card, Cards, Rank
from Utils import assertInstance
    
######################################################################
#
# Exceptions
#

class IncompleteHandException(PokerException):
    """Tried to get the rank of a hand that wasn't complete."""
    pass

######################################################################
#
# PokerRank
#

class PokerRank:

    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    TRIPS = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8

    handRankStrings = [
	"High Card",
	"Pair",
	"Two Pair",
	"Three of a kind",
	"Straight",
	"Flush",
	"Full House",
	"Four of a Kind",
	"Straight Flush"
	]

    # Ignore Straights when calculating rank
    ignoreStraights = False

    # Ignore flushes when calculating rank?
    ignoreFlushes = False

    # Return lowest rank?
    lowRank = False

    def __init__(self, hand):
	assertInstance(hand, Cards)
	self.hand = hand
	self.rank = None
	self.primaryCard = None
	self.secondaryCard = None
	self.kickers = None
	if self.lowRank:
	    Rank.acesAreLow()
	else:
	    Rank.acesAreHigh()
	for cards in hand.combinations(5):
	    rank = self.__getRank(cards)
	    replace = False
	    if self.rank is None:
		replace = True
	    else:
		comparison = cmp(self, rank)
		if (((not self.lowRank) and (comparison < 0)) or
		    (self.lowRank and (comparison > 0))):
		    replace = True
	    if replace:
		self.rank = rank.rank
		self.primaryCard = rank.primaryCard
		self.secondaryCard = rank.secondaryCard
		self.kickers = rank.kickers

    def __createRank(self, rankValue, primaryCard, secondaryCard, kickers):
	"""Create a new PokerRank object seeded with given parameters,
	without calling __init__."""
	import new
	rank = new.instance(PokerRank)
	rank.rank = rankValue
	rank.primaryCard = primaryCard
	rank.secondaryCard = secondaryCard
	rank.kickers = kickers
	return rank

    def __getRank(self, cards):
	"""Get rank of five cards."""
	cards.sort()
	isStraight = False
	isWheel = False
	isFlush = (not self.ignoreFlushes) and cards.sameSuit()
	if not self.ignoreStraights:
	    if cards.consecutivelyDescending():
		isStraight = True
	# Special case check for wheel (A2345)
	if ((not self.ignoreStraights) and
	    (not isStraight) and
	    (cards[0].rank == Rank.ACE) and
	    (cards[1].rank == Rank.FIVE) and
	    (cards[2].rank == Rank.FOUR) and
	    (cards[3].rank == Rank.THREE) and
	    (cards[4].rank == Rank.TWO)):
	    isWheel = True
	# Do we have a straight flush?
	if (isStraight and isFlush):
	    return self.__createRank(PokerRank.STRAIGHT_FLUSH, cards[0].rank,
				     None, cards[1:])
	if (isWheel and isFlush):
	    return self.__createRank(PokerRank.STRAIGHT_FLUSH, Rank(Rank.FIVE),
				     None, None)
	# Check for four of a kind
	if (cards[0].rank == cards[1].rank == cards[2].rank == cards[3].rank):
	    return self.__createRank(PokerRank.FOUR_OF_A_KIND, cards[0].rank,
				     None, cards[4:])
	if (cards[1].rank == cards[2].rank == cards[3].rank == cards[4].rank):
	    return self.__createRank(PokerRank.FOUR_OF_A_KIND, cards[0].rank,
				     None, cards[4:])
	# Check for full house
	#   -First two and last two cards must match
	#   -Then middle card either matches first two cards
	#    or last two cards
	if ((cards[0].rank == cards[1].rank) and
	    (cards[3].rank == cards[4].rank)):
	    if (cards[2].rank == cards[0].rank):
		# XXXYY
		return self.__createRank(PokerRank.FULL_HOUSE, cards[0].rank,
					 cards[3].rank, None)
	    elif (cards[2].rank == cards[3].rank):
		# XXYYY
		return self.__createRank(PokerRank.FULL_HOUSE, cards[2].rank,
					 cards[0].rank, None)
	# Check for flush, which we've already done
	if isFlush:
	    return self.__createRank(PokerRank.FLUSH, cards[0].rank,
				     None, cards[1:])
	# Check for Straight, which we've already done
	if isStraight:
	    return self.__createRank(PokerRank.STRAIGHT, cards[0].rank,
				     None, None)
	if isWheel:
	    return self.__createRank(PokerRank.STRAIGHT, Rank(Rank.FIVE),
				     None, None)
	# Check for trips
	if (cards[0].rank == cards[1].rank == cards[2].rank):
	    return self.__createRank(PokerRank.TRIPS, cards[0].rank,
				     None, cards[3:])
	if (cards[1].rank == cards[2].rank == cards[3].rank):
	    kickers = Cards()
	    kickers.append(cards[0])
	    kickers.append(cards[4])
	    return self.__createRank(PokerRank.TRIPS, cards[1].rank,
				     None, kickers)
	if (cards[2].rank == cards[3].rank == cards[4].rank):
	    return self.__createRank(PokerRank.TRIPS, cards[2].rank,
				     None, cards[:2])
	# Check for two pair	    
	# At this point we know we don't have trips, so can optimize some
	if (cards[0].rank == cards[1].rank):
	    if (cards[2].rank == cards[3].rank):
		return self.__createRank(PokerRank.TWO_PAIR, cards[0].rank,
					 cards[2].rank, cards[4:])
	    if (cards[3].rank == cards[4].rank):
		return self.__createRank(PokerRank.TWO_PAIR, cards[0].rank,
					 cards[3].rank, cards[2:3])
	if ((cards[1].rank == cards[2].rank) and
	    (cards[3].rank == cards[4].rank)):
	    return self.__createRank(PokerRank.TWO_PAIR, cards[1].rank,
				     cards[3].rank, cards[0:1])
	# Check for a pair
	# At this point we know we don't have two pair or trips
	foundPair = False
	for index in range(4):
	    if cards[index].rank == cards[index+1].rank:
		foundPair = True
		break
	if foundPair:
	    pairRank = cards[index].rank
	    del cards[index:index+2]
	    return self.__createRank(PokerRank.PAIR, pairRank, None, cards)
	# Just a high card
	return self.__createRank(PokerRank.HIGH_CARD, cards[0].rank,
				 None, cards[1:])

    def __str__(self):
	if self.rank == PokerRank.HIGH_CARD:
	    return "High card %s" % self.primaryCard.longString()
	if self.rank == PokerRank.PAIR:
	    return "Pair of %s" % self.primaryCard.pluralString()
	if self.rank == PokerRank.TWO_PAIR:
	    return "Two pair %s and %s" % (self.primaryCard.pluralString(),
					   self.secondaryCard.pluralString())
	if self.rank == PokerRank.THREE_OF_A_KIND:
	    return "Three of kind %s" % self.primaryCard.pluralString()
	if self.rank == PokerRank.STRAIGHT:
	    return "Straight %s high" % self.primaryCard.longString()
	if self.rank == PokerRank.FLUSH:
	    return "Flush %s high" % self.primaryCard.longString()
	if self.rank == PokerRank.FULL_HOUSE:
	    return "Full house %s full of %s" % (self.primaryCard.pluralString(),
						 self.secondaryCard.pluralString())
	if self.rank == PokerRank.FOUR_OF_A_KIND:
	    return "Four of a kind %s" % self.primaryCard.pluralString()
	if self.rank == PokerRank.STRAIGHT_FLUSH:
	    return "Straight flush %s high" % self.primaryCard.longString()
	raise PokerInternalException("Unknown rank %d" % self.rank)

    def kickersAsString(self):
	return str(self.kickers)

    def __cmp__(self, other):
	if other is None:
	    # Always greater than nothing
	    return 1
	# Allow comparison of PokerRank object and integer
	if isinstance(other, int):
	    return cmp(self.rank, other)
	assertInstance(other, PokerRank)
	if self.rank != other.rank:
	    return cmp(self.rank, other.rank)
	if self.primaryCard != other.primaryCard:
	    return cmp(self.primaryCard, other.primaryCard)
	if self.secondaryCard != other.secondaryCard:
	    return cmp(self.secondaryCard, other.secondaryCard)
	if self.kickers is not None:
	    for i in range(0, len(self.kickers)):
		# I seem to have an occassional exception here, so debug
		try:
		    if self.kickers[i] != other.kickers[i]:
			return cmp(self.kickers[i], other.kickers[i])
		except:
		    string = "Caught bad kicker comparison (i=%d/rank is %s)." % (i, str(self))
		    if self.kickers:
			string += "\nself.kickers = %s" % self.kickers
		    if other.kickers:
			string += "\nother.kickers = %s" % other.kickers
		    raise PokerInternalException("Bad kicker comparison\n" + string)
	# Truly equal
	return 0

class PokerLowRank(PokerRank):
    """Get the lowest poker rank of a hand, ignoring straights and flushes.
    The lowest possible rank is 5-high (5432A)."""
    ignoreStraights=True
    ignoreFlushes=True
    lowRank=True
    
    def __init__(self, hand):
	PokerRank.__init__(self, hand)

    def isEightOrBetter(self):
	"""Does rank qualify for eight or better low?"""
	return (self.rank == PokerRank.HIGH_CARD) and (self.primaryCard <= 8)

