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

from BitField import BitField
from PokerException import PokerException, PokerInternalException
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

class PokerRankBase(BitField):
    # Poker rank is a bitfield that looks like the following (each field
    # is a 4 bit nibble):
    #   -- Type PrimaryRank SecondaryRank Kicker1 Kicker2 Kicker3 Kicker4
    #
    # This is based on the strategy at:
    # See http://cowboyprogramming.com/2007/01/04/programming-poker-ai
    # With the modication that I have 4 kickers (for high card)

    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8

    # Some useful aliases
    TRIPS = THREE_OF_A_KIND
    BOAT = FULL_HOUSE
    QUADS = FOUR_OF_A_KIND

    # Offsets into BitField
    TYPE_OFFSET = 24
    PRIMARY_CARD_OFFSET =  20
    SECONDARY_CARD_OFFSET = 16
    FIRST_KICKER_OFFSET = 12
    SECOND_KICKER_OFFSET = 8
    THIRD_KICKER_OFFSET = 4
    FOURTH_KICKER_OFFSET = 0

    handRankTemplates = [
	"High Card $primaryRank",
	"Pair of $primaryRankPlural",
	"Two Pair $primaryRankPlural and $secondaryRankPlural",
	"Three of a kind $primaryRankPlural",
	"Straight $primaryRank high",
	"Flush $primaryRank high",
	"Full House $primaryRankPlural full of $secondaryRankPlural",
	"Four of a Kind $primaryRankPlural",
	"Straight Flush $primaryRank high"
	]

    def __init__(self, rankValue=None, primaryCard=None,
		 secondaryCard=None, kickers=None):
        BitField.__init__(self, value = 0, length=32)
        if rankValue:
            self.setType(rankValue)
        if primaryCard:
            self.setPrimaryCardRank(primaryCard)
        if secondaryCard:
            self.setSecondaryCardRank(secondaryCard)
        if kickers:
            self.setKickers(kickers)

    @staticmethod
    def straightFlush(rank):
	return PokerRankBase(PokerRankBase.STRAIGHT_FLUSH, rank, None, None)

    @staticmethod
    def quads(rank, kickers):
	return PokerRankBase(PokerRankBase.QUADS, rank, None, kickers)

    @staticmethod
    def fullHouse(primaryRank, secondaryRank):
	return PokerRankBase(PokerRankBase.BOAT,
			     primaryRank,
			     secondaryRank,
			     None)

    @staticmethod
    def flush(rank, kickers):
	return PokerRankBase(PokerRankBase.FLUSH, rank, None, kickers)

    @staticmethod
    def straight(rank):
	return PokerRankBase(PokerRankBase.STRAIGHT, rank, None, None)

    @staticmethod
    def trips(rank, kickers):
	return PokerRankBase(PokerRankBase.TRIPS, rank, None, kickers)

    @staticmethod
    def twoPair(primaryRank, secondaryRank, kickers):
	return PokerRankBase(PokerRankBase.TWO_PAIR,
			     primaryRank,
			     secondaryRank,
			     kickers)

    @staticmethod
    def pair(rank, kickers):
	return PokerRankBase(PokerRankBase.PAIR, rank, None, kickers)

    @staticmethod
    def highCard(rank, kickers):
	return PokerRankBase(PokerRankBase.HIGH_CARD, rank, None, kickers)

    def __str__(self):
	if self.value == 0:
	    raise PokerException("Tried to convert uninitialized PokerRank to string.")
        type = self.getType()
	try:
	    template = self.handRankTemplates[type]
	except:
	    raise PokerException("Unknown rank %d" % type)
	from string import Template
	s = Template(template)
        primaryRank = self.getPrimaryCardRank()
	d = dict(primaryRank=primaryRank.longString(),
		 primaryRankPlural=primaryRank.pluralString())
        secondaryRank = self.getSecondaryCardRank()
	if secondaryRank:
	    d['secondaryRank']=secondaryRank.longString()
	    d['secondaryRankPlural']=secondaryRank.pluralString()
	return s.substitute(d)

    def debugString(self):
        """Return descriptive string for debugging."""
        string = "%0X" % self.value
        if self.value:
            string += ":" + self.__str__()
        string += ":kickers " + self.kickersAsString()
        return string

    def kickersAsString(self):
        kickers = self.getKickerRanks()
        string = ''
        for kicker in kickers:
            if kicker:
                string = string + str(kicker) + ' '
	return string

    def __cmp__(self, other):
	if other is None:
	    # Always greater than nothing
	    return 1
	# Allow comparison of PokerRank object and integer
	if isinstance(other, int):
	    return cmp(self.getType(), other)
	assertInstance(other, PokerRankBase)
        return cmp(self.value, other.value)

    # Override methods set by BitField
    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def _setEqual(self, otherRank):
	"""This this rank equal to provided rank."""
	self.value = otherRank.value

    # Get/Set functions for bit fields
    def setType(self, type):
        """Set the type (e.g. FULL_HOUSE, STRAIGHT) of this instance."""
        self.setBitRange(numBits = 4, value=type, offset=self.TYPE_OFFSET)

    def getType(self):
        """Return the type of this instance as an integer."""
        return self.getBitRange(numBits = 4, offset=self.TYPE_OFFSET, shift=True)

    def setPrimaryCardRank(self, rank):
        """Set the rank of the primary card."""
        if isinstance(rank, Card):
            rank = rank.rank
        self.setBitRange(numBits=4,
                         value=rank,
                         offset=self.PRIMARY_CARD_OFFSET)

    def getPrimaryCardRank(self):
        """Get the rank of the primary card.

        Returns None if no rank defined."""
        value = self.getBitRange(numBits = 4,
                                 offset=self.PRIMARY_CARD_OFFSET,
                                 shift=True)
        if not value:
            return None
        return Rank(value)

    def setSecondaryCardRank(self, rank):
        """Set the rank of the secondary card (e.g. the pair in a full house)."""
        if isinstance(rank, Card):
            rank = rank.rank
        self.setBitRange(numBits = 4,
                         value=rank,
                         offset=self.SECONDARY_CARD_OFFSET)

    def getSecondaryCardRank(self):
        """Get the rank of the secodary card (e.g. the pair in a full house).

        Returns None if no rank defined."""
        value = self.getBitRange(numBits = 4,
                                 offset=self.SECONDARY_CARD_OFFSET,
                                 shift=True)
        if not value:
            return None
        return Rank(value)

    def setKickers(self, kickers):
        """Set (up to 4) kickers."""
        # We want highest kicker first
        kickers.sort(reverse=True)
        offset = self.FIRST_KICKER_OFFSET
        for kicker in kickers:
            # All for kicker to be both card or Rank
            if isinstance(kicker, Card):
                kickerRank = kicker.rank
            else:
                kickerRank = kicker
            self.setBitRange(numBits = 4,
                             offset=offset,
                             value=kickerRank)
            offset -= 4

    def getKickerRanks(self):
        """Return an array with ranks of kickers."""
        kickers = []
        offset = self.FIRST_KICKER_OFFSET
        while offset >= 0:
            value = self.getBitRange(numBits=4,
                                     offset=offset,
                                     shift=True)
            if value == 0:
                break
            kickers.append(Rank(value))
            offset -= 4
        return kickers

    def isEightOrBetterLow(self):
	"""Does rank qualify for eight or better low?"""
	return ((self.getType() == PokerRank.HIGH_CARD) and
                (self.getPrimaryCardRank() <= 8))

######################################################################
#
# PokerRank
#

class PokerRank(PokerRankBase):
    def __init__(self, hand):
	assertInstance(hand, Cards)
	PokerRankBase.__init__(self)
	self.hand = hand
	for cards in hand.hands():
	    if len(cards) > 5:
		rank = self.__getRankSixPlusCards(cards)
	    else:
		rank = self.__getRankFiveCards(cards)
	    if self < rank:
		self._setEqual(rank)

    def __getRankFiveCards(self, cards):
	"""Get rank of five cards. This method is more efficient than
	__getRankSixPlusCards()."""
	cards.sort()
	straight = False
	wheel = False
	isFlush = cards.sameSuit()
	straight = isStraight(cards)
	wheel = isWheel(cards)
	# Do we have a straight flush?
	if (straight and isFlush):
	    return self.straightFlush(cards[0].rank)
	if (wheel and isFlush):
	    return self.straightFlush(cards[1].rank)
	# Check for four of a kind
	if (cards[0].rank == cards[1].rank == cards[2].rank == cards[3].rank):
	    return self.quads(cards[0].rank, cards[4:])
	if (cards[1].rank == cards[2].rank == cards[3].rank == cards[4].rank):
	    return self.quads(cards[1].rank, cards[0:1])
	# Check for full house
	#   -First two and last two cards must match
	#   -Then middle card either matches first two cards
	#    or last two cards
	if ((cards[0].rank == cards[1].rank) and
	    (cards[3].rank == cards[4].rank)):
	    if (cards[2].rank == cards[0].rank):
		# XXXYY
		return self.fullHouse(cards[0].rank, cards[3].rank)
	    elif (cards[2].rank == cards[3].rank):
		# XXYYY
		return self.fullHouse(cards[2].rank, cards[0].rank)
	# Check for flush, which we've already done
	if isFlush:
	    return self.flush(cards[0].rank, cards[1:])
	# Check for Straight, which we've already done
	if straight:
	    return self.straight(cards[0].rank)
	if wheel:
	    return self.straight(cards[1].rank)
	# Check for trips
	if ((cards[0].rank == cards[1].rank == cards[2].rank) or
	    (cards[1].rank == cards[2].rank == cards[3].rank) or
	    (cards[2].rank == cards[3].rank == cards[4].rank)):
	    # cards[2] will always be one of the trips
	    primaryRank = cards[2].rank
	    cards.removeRank(primaryRank)
	    return self.trips(primaryRank, cards)
	# Check for two pair	    
	# At this point we know we don't have trips, so can optimize some
	if (cards[0].rank == cards[1].rank):
	    if (cards[2].rank == cards[3].rank):
		return self.twoPair(cards[0].rank, cards[2].rank, cards[4:])
	    if (cards[3].rank == cards[4].rank):
		return self.twoPair(cards[0].rank, cards[3].rank, cards[2:3])
	elif ((cards[1].rank == cards[2].rank) and
	      (cards[3].rank == cards[4].rank)):
	    return self.twoPair(cards[1].rank, cards[3].rank, cards[0:1])
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
	    return self.pair(pairRank, cards)
	# Just a high card
	return self.highCard(cards[0].rank, cards[1:])

    def __getRankSixPlusCards(self, cards):
	"""Get high rank from six or more cards."""
	cards.sort()
	straight = findLongestStraight(cards)
	# Check for straight flush
	if (len(straight) >= 5) and straight.sameSuit():
	    return self.straightFlush(straight[0].rank)
	rankCount = cards.countRanks()
	# Check for four of a kind
	try:
	    primaryRank = rindex(rankCount, 4)
	except:
	    pass
	else:
	    cards.removeRank(primaryRank)
	    return self.quads(primaryRank, cards[0:1])
	# Check for full house
	count = rankCount.count(3)
	if count > 1:
	    primaryRank = rindex(rankCount, 3)
	    # Set that value to zero so we can find second value
	    rankCount[primaryRank] = 0
	    secondaryRank = rindex(rankCount, 3)
	    return self.fullHouse(primaryRank,secondaryRank)
	elif count == 1:
	    try:
		secondaryRank = rindex(rankCount, 2)
	    except:
		pass
	    else:
		primaryRank = rindex(rankCount, 3)
		return self.fullHouse(primaryRank, secondaryRank)
	# Check for flush
	# Assume we will find only one flush
	for suit in Suit.suits:
	    if cards.suitCount(suit) >= 5:
		suitedCards = cards.suitedCards(suit)
		topCard = suitedCards.pop(0)
		primaryRank = topCard.rank
		return self.flush(primaryRank, suitedCards[:4])
	# Check for straight
	if len(straight) >= 5:
	    return self.straight(straight[0].rank)
	# Check for trips
	try:
	    primaryRank = rindex(rankCount, 3)
	except:
	    pass
	else:
	    cards.removeRank(primaryRank)
	    return self.trips(primaryRank, cards[0:2])
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
	    return self.twoPair(primaryRank, secondaryRank, cards[0:1])
	elif pairCount == 1:
	    primaryRank = rankCount.index(2)
	    cards.removeRank(primaryRank)
	    return self.pair(primaryRank, cards[0:3])
	# High card
	primaryRank = cards.pop(0).rank
	return self.highCard(primaryRank, cards[0:4])

######################################################################
#
# PokerLowRank
#

class PokerLowRank(PokerRankBase):
    """Get the lowest poker rank of a hand, ignoring straights and flushes.
    The lowest possible rank is 5-high (5432A)."""
    
    def __init__(self, hand):
	assertInstance(hand, Cards)
        # Start with highest possible rank and work down
	PokerRankBase.__init__(self, PokerRankBase.STRAIGHT_FLUSH, Rank.ACE, None, None)
	self.hand = hand
        self.hand.makeAcesLow()
	for cards in hand.hands():
	    rank = self.__getLowRank(cards)
	    if rank < self:
		self._setEqual(rank)

    def isEightOrBetter(self):
	"""Does rank qualify for eight or better low?"""
	return ((self.getType() == PokerRank.HIGH_CARD) and
                (self.getPrimaryCardRank() <= 8))

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
	    return self.highCard(primaryRank, lowestCards)
	elif countLevel == 2:
	    # We have at least one pair. Do we have two pair?
	    rankCount = lowestCards.countRanks()
	    if rankCount.count(2) == 2:
		primaryRank = rindex(rankCount, 2)
		secondaryRank = rankCount.index(2)
		lowestCards.removeRank(primaryRank)
		lowestCards.removeRank(secondaryRank)
		return self.twoPair(primaryRank, secondaryRank, lowestCards)
	    else:
		# Just a single pair
		primaryRank = rankCount.index(2)
		lowestCards.removeRank(primaryRank)
		return self.pair(primaryRank, lowestCards)
	elif countLevel == 3:
	    # We have at least trips or maybe a full house
	    rankCount = lowestCards.countRanks()
	    if rankCount.count(2) == 1:
		primaryRank = rankCount.index(3)
		secondaryRank = rankCount.index(2)
		return self.fullHouse(primaryRank, secondaryRank)
	    else:
		# Just trips
		primaryRank = rankCount.index(3)
		lowestCards.removeRank(primaryRank)
		return self.trips(primaryRank, lowestCards)
	else:
	    # We've got quads (assuming no five of a kind)
	    rankCount = lowestCards.countRanks()
	    primaryRank = rankCount.index(4)
	    lowestCards.removeRank(primaryRank)
	    return self.quads(primaryRank, lowestCards)

######################################################################
#
# HoldEmStartingHandRank
#

class HoldEmStartingHandRank(PokerRankBase):
    """Get the rank of two starting cards in HoldEmHand."""
    
    def __init__(self, hand):
	from Hand import HoldEmHand
	assertInstance(hand, HoldEmHand)
	if len(hand) != 2:
	    raise IncompleteHandException("Need 2 cards in hand, have %d" % len(hand))
	PokerRankBase.__init__(self)
	if hand[0] == hand[1]:
	    # Pair
	    self.rank = PokerRank.PAIR
	    self.primaryCard = hand[0]
	else:
	    # Two unpaired cards, find higher
	    self.rank = PokerRank.HIGH_CARD
	    if hand[0] > hand[1]:
		self.primaryCard = hand[0].rank
		self.kickers = [hand[1]]
	    else:
		self.primaryCard = hand[1].rank
		self.kickers = [hand[0]]

######################################################################
#
# Utility Functions
#


def findLongestStraight(cards):
    """Given an array of sorted cards, return the longest straight."""
    if len(cards) == 0:
	return Cards()
    longestStraight = Cards()
    straight = Cards()
    straight.append(cards[0])
    for index in range(1,len(cards)):
	if cards[index].rank != (straight[len(straight)-1].rank - 1):
	    if len(straight) > len(longestStraight):
		longestStraight = straight
	    straight = Cards()
	straight.append(cards[index])
    if len(straight) > len(longestStraight):
	longestStraight = straight
    # Check for special case of straight ending with a 2 when we have
    # and Ace, in which case treat the ace as low.
    if ((longestStraight[len(longestStraight)-1].rank == Rank.TWO) and
	(cards[0].rank == Rank.ACE)):
	longestStraight.append(cards[0])
    return longestStraight

def isStraight(cards):
    """Do five sorted cards form a straight? (Excluding wheel.)"""
    if ((cards[1].rank == (cards[0].rank - 1)) and
	(cards[2].rank == (cards[1].rank - 1)) and
	(cards[3].rank == (cards[2].rank - 1)) and
	(cards[4].rank == (cards[3].rank - 1))):
	return True
    return False

def isWheel(cards):
    """Do five sorted card form a wheel (5432A)?"""
    if ((cards[0].rank == Rank.ACE) and
	(cards[1].rank == Rank.FIVE) and
	(cards[2].rank == Rank.FOUR) and
	(cards[3].rank == Rank.THREE) and
	(cards[4].rank == Rank.TWO)):
	return True
    return False
