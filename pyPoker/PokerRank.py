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
from Cards import Card, Cards, Rank, Suit
from Hand import CommunityCardHand
from Utils import assertInstance, rindex
    
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
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8

    TRIPS = THREE_OF_A_KIND
    BOAT = FULL_HOUSE
    QUADS = FOUR_OF_A_KIND

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
	for cards in hand.hands():
	    if self.lowRank:
		rank = self.__getLowRank(cards)
	    else:
		rank = self.__getRankFromSevenCards(cards)
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

    def __getRankFromSevenCards(self, cards):
	cards.sort()
	straight = cards.findStraight()
	# Check for straight flush
	if (len(straight) >= 5) and straight.sameSuit():
	    return self.__createRank(PokerRank.STRAIGHT_FLUSH,
				     Rank(straight[0].rank),
				     None,
				     straight[1:5])
	rankCount = cards.countRanks()
	# Check for four of a kind
	try:
	    primaryRank = rindex(rankCount, 4)
	except:
	    pass
	else:
	    cards.removeRank(primaryRank)
	    return self.__createRank(PokerRank.FOUR_OF_A_KIND,
				     Rank(primaryRank),
				     None,
				     cards[0:1])
	# Check for full house
	count = rankCount.count(3)
	if count > 1:
	    primaryRank = rindex(rankCount, 3)
	    # Set that value to zero so we can find second value
	    rankCount[primaryRank] = 0
	    secondaryRank = rindex(rankCount, 3)
	    return self.__createRank(PokerRank.FULL_HOUSE,
				     Rank(primaryRank),
				     Rank(secondaryRank),
				     None)
	elif count == 1:
	    try:
		secondaryRank = rindex(rankCount, 2)
	    except:
		pass
	    else:
		primaryRank = rindex(rankCount, 3)
		return self.__createRank(PokerRank.FULL_HOUSE,
					 Rank(primaryRank),
					 Rank(secondaryRank),
					 None)
	# Check for flush
	for suit in Suit.suits:
	    if cards.suitCount(suit) >= 5:
		suitedCards = cards.suitedCards(suit)
		topCard = suitedCards.pop(0)
		primaryRank = topCard.rank
		return self.__createRank(PokerRank.FLUSH,
					 Rank(primaryRank),
					 None,
					 suitedCards[:4])
	# Check for straight
	if len(straight) >= 5:
	    return self.__createRank(PokerRank.STRAIGHT,
				     Rank(straight[0].rank),
				     None,
				     None)
	# Check for trips
	try:
	    primaryRank = rindex(rankCount, 3)
	except:
	    pass
	else:
	    cards.removeRank(primaryRank)
	    return self.__createRank(PokerRank.THREE_OF_A_KIND,
				     Rank(primaryRank),
				     None,
				     cards[0:2])
	# Check for two pair and pair
	pairCount = rankCount.count(2)
	if pairCount > 1:
	    # Two pair
	    primaryRank = rindex(rankCount, 2)
	    # Remove so we can find second pair
	    rankCount[primaryRank] = 0
	    secondaryRank = rindex(rankCount, 2)
	    cards.removeRank(primaryRank)
	    cards.removeRank(secondaryRank)
	    return self.__createRank(PokerRank.TWO_PAIR,
				     Rank(primaryRank),
				     Rank(secondaryRank),
				     cards[0:1])
	elif pairCount == 1:
	    primaryRank = rankCount.index(2)
	    cards.removeRank(primaryRank)
	    return self.__createRank(PokerRank.PAIR,
				     Rank(primaryRank),
				     None,
				     cards[0:3])
	# High card
	primaryRank = cards.pop(0).rank
	return self.__createRank(PokerRank.HIGH_CARD,
				 Rank(primaryRank),
				 None,
				 cards[0:4])

    def __getLowRank(self, cards):
	"""Find lowest rank of given cards ignoring straights and flushes."""
	cards.sort()
	# Find the lowest five cards
	# Add each lowest card that doesn't pair to our created array.
	# If we don't get five start then with the lowest that pairs, then
	# the lowest that forms trips, etc.
	countLevel = 1
	lowestCards = Cards()
	remainingCards = Cards()
	while len(lowestCards) < 5:
	    if len(cards) == 0:
		# Didn't find enough, so now get cards that match cards
		# in lowestCards (or match pairs in lowestCards and so on)
		cards = remainingCards
		remainingCards = Cards()
		countLevel += 1
	    card = cards.pop()
	    if lowestCards.rankCount(card.rank) < countLevel:
		lowestCards.insert(0, card)
	    else:
		remainingCards.insert(0, card)
	# Ok, lowestCards now contain five lowest cards
	if countLevel == 1:
	    # We didn't have to pair, so it's a high card
	    primaryRank = lowestCards.pop(0).rank
	    return self.__createRank(PokerRank.HIGH_CARD,
				     Rank(primaryRank),
				     None,
				     lowestCards)
	elif countLevel == 2:
	    # We have at least one pair. Do we have two pair?
	    rankCount = lowestCards.countRanks()
	    if rankCount.count(2) == 2:
		primaryRank = rindex(rankCount, 2)
		secondaryRank = rankCount.index(2)
		lowestCards.removeRank(primaryRank)
		lowestCards.removeRank(secondaryRank)
		return self.__createRank(PokerRank.TWO_PAIR,
					 Rank(primaryRank),
					 Rank(secondaryRank),
					 lowestCards)
	    else:
		# Just a single pair
		primaryRank = rankCount.index(2)
		lowestCards.removeRank(primaryRank)
		return self.__createRank(PokerRank.PAIR,
					 Rank(primaryRank),
					 None,
					 lowestCards)
	elif countLevel == 3:
	    # We have at least trips or maybe a full house
	    rankCount = lowestCards.countRanks()
	    if rankCount.count(2) == 1:
		primaryRank = rankCount.index(3)
		secondaryRank = rankCount.index(2)
		return self.__createRank(PokerRank.FULL_HOUSE,
					 Rank(primaryRank),
					 Rank(secondaryRank),
					 None)
	    else:
		# Just trips
		primaryRank = rankCount.index(3)
		lowestCards.removeRank(primaryRank)
		return self.__createRank(PokerRank.TRIPS,
					 Rank(primaryRank),
					 None,
					 lowestCards)
	else:
	    # We've got quads
	    rankCount = lowestCards.countRanks()
	    primaryRank = rankCount.index(4)
	    lowestCards.removeRank(primaryRank)
	    return self.__createRank(PokerRank.QUADS,
				     Rank(primaryRank),
				     None,
				     lowestCards)

    def __getLowestFiveCards(self, cards):
	"""Return lowest five cards ignoring straights and flushes."""
	
	    
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

class HoldEmStartingHandRank(PokerRank):
    """Get the rank of two starting cards in HoldEmHand."""
    
    def __init__(self, hand):
	from Hand import HoldEmHand
	assertInstance(hand, HoldEmHand)
	if len(hand) != 2:
	    raise IncompleteHandException("Need 2 cards in hand, have %d" % len(hand))
	self.rank = None
	self.primaryCard = None
	self.secondaryCard = None
	self.kickers = None
	if hand[0] == hand[1]:
	    # Pair
	    self.rank = PokerRank.PAIR
	    self.primaryCard = hand[0]
	else:
	    # Two unpaired cards, find higher
	    self.rank = PokerRank.HIGH_CARD
	    if hand[0] > hand[1]:
		self.primaryCard = hand[0]
		self.kickers = [hand[1]]
	    else:
		self.primaryCard = hand[1]
		self.kickers = [hand[0]]

					  
