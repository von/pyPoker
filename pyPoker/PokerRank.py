"""Class for representing a Hand's rank."""

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

class PokerRank(BitField):
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

    @staticmethod
    def __new__(cls, rankValue, primaryCard=None,
		 secondaryCard=None, kickers=None):
        # TODO: Add sanity checking of valyes
        value = rankValue << cls.TYPE_OFFSET

        # Alow primaryCard to be Card or Rank
        # TODO: This slows us down, allow only Rank
        if primaryCard:
            if isinstance(primaryCard, Card):
                rank = primaryCard.rank
            else:
                rank = primaryCard
            value |= rank << cls.PRIMARY_CARD_OFFSET

        if secondaryCard:
            if isinstance(secondaryCard, Card):
                rank = secondaryCard.rank
            else:
                rank = secondaryCard
            value |= rank << cls.SECONDARY_CARD_OFFSET
        
        if kickers:
            kickers.sort(reverse=True)
            offset = cls.FIRST_KICKER_OFFSET
            for kicker in kickers:
                # All for kicker to be both card or Rank
                if isinstance(kicker, Card):
                    kickerRank = kicker.rank
                else:
                    kickerRank = kicker
                value |= kickerRank << offset
                offset -= 4

        # Sanity check
        if value == 0:
            raise PokerInternalException("Value == 0")

        return BitField.__new__(cls, value)

    @staticmethod
    def straightFlush(rank):
	return PokerRank(PokerRank.STRAIGHT_FLUSH, rank, None, None)

    @staticmethod
    def quads(rank, kickers):
	return PokerRank(PokerRank.QUADS, rank, None, kickers)

    @staticmethod
    def fullHouse(primaryRank, secondaryRank):
	return PokerRank(PokerRank.BOAT,
                         primaryRank,
                         secondaryRank,
                         None)

    @staticmethod
    def flush(rank, kickers):
	return PokerRank(PokerRank.FLUSH, rank, None, kickers)

    @staticmethod
    def straight(rank):
	return PokerRank(PokerRank.STRAIGHT, rank, None, None)

    @staticmethod
    def trips(rank, kickers):
	return PokerRank(PokerRank.TRIPS, rank, None, kickers)

    @staticmethod
    def twoPair(primaryRank, secondaryRank, kickers):
	return PokerRank(PokerRank.TWO_PAIR,
                         primaryRank,
                         secondaryRank,
                         kickers)

    @staticmethod
    def pair(rank, kickers):
	return PokerRank(PokerRank.PAIR, rank, None, kickers)

    @staticmethod
    def highCard(rank, kickers):
	return PokerRank(PokerRank.HIGH_CARD, rank, None, kickers)

    def __str__(self):
	if self == 0:
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

    def getType(self):
        """Return the type of this instance as an integer."""
        return self.getBitRange(numBits = 4, offset=self.TYPE_OFFSET, shift=True)
    def getPrimaryCardRank(self):
        """Get the rank of the primary card.

        Returns None if no rank defined."""
        value = self.getBitRange(numBits = 4,
                                 offset=self.PRIMARY_CARD_OFFSET,
                                 shift=True)
        if not value:
            return None
        return Rank(value)

    def getSecondaryCardRank(self):
        """Get the rank of the secodary card (e.g. the pair in a full house).

        Returns None if no rank defined."""
        value = self.getBitRange(numBits = 4,
                                 offset=self.SECONDARY_CARD_OFFSET,
                                 shift=True)
        if not value:
            return None
        return Rank(value)

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

