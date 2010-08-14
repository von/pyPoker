"""Class for ranking poker hands"""

from BitField import BitField
from Cards import Rank, Suit
from PokerException import PokerInternalException
from PokerRank import PokerRank

class RankerBase:
    """Base class for other Ranker classes (low and high)."""

    @classmethod
    def _handToSuitedBitFields(cls, hand):
        """Given a hand, return a array of four BitFields, one per suit, indicating what card ranks the hand contains."""
        bitfields = [None] * (Suit.SPADES + 1)
        bitfields[Suit.CLUBS] = BitField(0)
        bitfields[Suit.DIAMONDS] = BitField(0)
        bitfields[Suit.HEARTS] = BitField(0)
        bitfields[Suit.SPADES] = BitField(0)
        for card in hand:
            bitfields[card.suit].setBit(card.rank)
        return bitfields

    @classmethod
    def _handToBitField(cls, hand):
        """Given a hand, return a BitField including what card ranks the hand contians."""
        bitfield = BitField()
        for card in hand:
            bitfield.setBit(card.rank)
        return bitfield

    @classmethod
    def _suitedBitFieldsToRankedBitFields(cls, bitfields):
        """Given an array of bitfields representing cards of the different suits, return a set of bitfields representing singletons, pairs, trips and quads."""
        # AND of all four fields results in bitfield of quads
        quadsBitField = (bitfields[Suit.CLUBS] & bitfields[Suit.DIAMONDS] &
                         bitfields[Suit.HEARTS] & bitfields[Suit.SPADES])
        # XOR of all four fields results in bitfield of ( singletons | trips )
        xorBitField = (bitfields[Suit.CLUBS] ^ bitfields[Suit.DIAMONDS] ^
                       bitfields[Suit.HEARTS] ^ bitfields[Suit.SPADES])
        # OR of ANDs results in bitfield of (Trips | Quads)
        andOrBitField = ((bitfields[Suit.CLUBS] & bitfields[Suit.DIAMONDS]) |
                         (bitfields[Suit.HEARTS] & bitfields[Suit.SPADES]))
        # Trips = (Trips | Quads ) & (Singletons | Trips)
        tripsBitField = xorBitField & andOrBitField
        # OR of all four fields results in bitfield of (singletons | pairs
        # | trips | quads)
        orBitField = (bitfields[Suit.CLUBS] | bitfields[Suit.DIAMONDS] |
                      bitfields[Suit.HEARTS] | bitfields[Suit.SPADES])
        # Pairs = (singletons | pairs | trips | quads) ^ (Singletons | Trips)
        #         ^ quads
        pairsBitField = orBitField ^ xorBitField ^ quadsBitField
        # Singletons = (Singletons | Trips) ^ Trips
        singletonsBitField = xorBitField ^ tripsBitField
        return (singletonsBitField, pairsBitField, tripsBitField, quadsBitField)

    # Lookup table for masks representing straights
    _straightBitFields = [
        # Straight rank, BitField value
        (Rank.ACE,   0x7c00),
        (Rank.KING,  0x3e00),
        (Rank.QUEEN, 0x1f00),
        (Rank.JACK,  0x0f80),
        (Rank.TEN,   0x07c0),
        (Rank.NINE,  0x03e0),
        (Rank.EIGHT, 0x01f0),
        (Rank.SEVEN, 0x00f8),
        (Rank.SIX,   0x007c),
        (Rank.FIVE,  0x003e),
        # Special case for wheel with ace high
        (Rank.FIVE,  0x403c)
        ]

    @classmethod
    def _hasStraight(cls, bitfield):
        """Does given bitfield represent a straight?

        Returns rank of highest straight or None if one not present."""
        for rank, bits in cls._straightBitFields:
            if bitfield.testBits(bits):
                return rank
        return None

    @classmethod
    def _isStraight(cls, cards):
        """Does the given five sorted cards represent a straight?

        Returns Rank of straight or None if not a straight."""
        if ((cards[1].rank == (cards[0].rank - 1)) and
            (cards[2].rank == (cards[1].rank - 1)) and
            (cards[3].rank == (cards[2].rank - 1)) and
            (cards[4].rank == (cards[3].rank - 1))):
            return cards[0].rank
        # Specical case for wheel with ACE high.
        if ((cards[0].rank == Rank.ACE) and
            (cards[1].rank == Rank.FIVE) and
            (cards[2].rank == Rank.FOUR) and
            (cards[3].rank == Rank.THREE) and
            (cards[4].rank == Rank.TWO)):
            return Rank.FIVE
        return False

class Ranker(RankerBase):
    """Given a Hand, return its PokerRank for its best high hand."""

    @classmethod
    def rankHand(cls, hand):
        """Given a Hand return a PokerRank for its best hand.

        Limited to Hands of five to seven cards."""
        highRank = None
        # Iterate through all the possible sets of cards in hand and
        # find the highest rank
        for cards in hand.hands():
            try:
                if len(cards) == 5:
                    rank = cls._rankFiveCardHand(cards)
                else:
                    rank = cls._rankSixOrSevenCardHand(cards)
            except Exception as e:
                import sys
                msg = "Error ranking hand %s: %s" % (cards, e)
                raise PokerInternalException, msg, sys.exc_info()[2]
    
            if (highRank is None) or (rank > highRank):
                highRank = rank
        return highRank

    @classmethod
    def _rankSixOrSevenCardHand(cls, cards):
        """Given a set of 6 or 7 cards, return a PokerRank for its best hand.

        Will work for 5 cards, but is less efficient than _rankFiveCardHand()."""
        if len(cards) > 7:
            raise ValueError("Hand has too many cards (%d > 7)" % len(cards))
        if len(cards) < 5:
            raise ValueError("Hand has too few cards (%d < 5)" % len(cards))

        # Array of bitfields of cards by suit
        suitedBitFields = cls._handToSuitedBitFields(cards)
        
        # Check for straight-flush
        highRank = None
        for suit in Suit.suits:
            rank = cls._hasStraight(suitedBitFields[suit])
            if rank and ((highRank is None) or (rank > highRank)):
                highRank = rank
        if highRank is not None:
            return PokerRank.straightFlush(highRank)

        # Get bitfields representing singletons, pairs, trips and quads
        (singletonsBitField,
         pairsBitField,
         tripsBitField,
         quadsBitField) = cls._suitedBitFieldsToRankedBitFields(suitedBitFields)

        # Single bitfield with all four suits merged for kickers and straights
        bitfield = (suitedBitFields[Suit.CLUBS] |
                    suitedBitFields[Suit.DIAMONDS] |
                    suitedBitFields[Suit.HEARTS] |
                    suitedBitFields[Suit.SPADES])

        # Check for quads
        if quadsBitField.setCount() > 0:
            rank = quadsBitField.highestSet()
            # Highest remaining card is our kicker
            bitfield.clearBit(rank)
            kickerRank = bitfield.highestSet()
            return PokerRank.quads(rank, [kickerRank])
            
        # Check for full house
        if ((tripsBitField > 0) & (pairsBitField > 0)):
            return PokerRank.fullHouse(tripsBitField.highestSet(),
                                       pairsBitField.highestSet())

        # Check for flush
        flushBitField = None
        for suit in Suit.suits:
            if suitedBitFields[suit].setCount() >= 5:
                if ((flushBitField is None) or
                    (suitedBitFields[suit] > flushBitField)):
                    flushBitField = suitedBitFields[suit]
        if flushBitField:
            rank = flushBitField.highestSet()
            flushBitField.clearBit(rank)
            kickers = flushBitField.highestNSet(4)
            return PokerRank.flush(rank, kickers)

        # Check for straight
        # We don't care about suit anymore so can just operate on bitfield
        rank = cls._hasStraight(bitfield)
        if rank:
            return PokerRank.straight(rank)

        # Check for trips
        if (tripsBitField > 0):
            rank = tripsBitField.highestSet()
            bitfield.clearBit(rank)
            kickers = bitfield.highestNSet(2)
            return PokerRank.trips(rank, kickers)

        # Check for two pair
        if (pairsBitField.setCount() > 1):
            ranks = pairsBitField.highestNSet(2)
            bitfield.clearBit(ranks[0])
            bitfield.clearBit(ranks[1])
            kicker = bitfield.highestSet()
            return PokerRank.twoPair(ranks[0], ranks[1], [kicker])

        # Check for pair
        if (pairsBitField > 0):
            rank = pairsBitField.highestSet()
            bitfield.clearBit(rank)
            kickers = bitfield.highestNSet(3)
            return PokerRank.pair(rank, kickers)

        # High card
        highCard = bitfield.highestSet()
        bitfield.clearBit(highCard)
        kickers = bitfield.highestNSet(4)
        return PokerRank.highCard(highCard, kickers)

    @classmethod
    def _rankFiveCardHand(cls, cards):
	"""Get rank of five cards. This method is more efficient than
	_getRankSixPlusCards()."""
	cards.sort(reverse=True)
	isFlush = cards.sameSuit()
	straightRank = cls._isStraight(cards)
	# Do we have a straight flush?
	if (straightRank and isFlush):
	    return PokerRank.straightFlush(straightRank)
	# Check for four of a kind
	if (cards[0].rank == cards[1].rank == cards[2].rank == cards[3].rank):
	    return PokerRank.quads(cards[0].rank, cards[4:])
	if (cards[1].rank == cards[2].rank == cards[3].rank == cards[4].rank):
	    return PokerRank.quads(cards[1].rank, cards[0:1])
	# Check for full house
	#   -First two and last two cards must match each other
	#   -Then middle card either matches first two cards
	#    or last two cards
	if ((cards[0].rank == cards[1].rank) and
	    (cards[3].rank == cards[4].rank)):
	    if (cards[2].rank == cards[0].rank):
		# XXXYY
		return PokerRank.fullHouse(cards[0].rank, cards[3].rank)
	    elif (cards[2].rank == cards[3].rank):
		# XXYYY
		return PokerRank.fullHouse(cards[2].rank, cards[0].rank)
	# Check for flush, which we've already done
	if isFlush:
	    return PokerRank.flush(cards[0].rank, cards[1:])
	# Check for Straight, which we've already done
	if straightRank:
	    return PokerRank.straight(straightRank)
	# Check for trips
	if ((cards[0].rank == cards[1].rank == cards[2].rank) or
	    (cards[1].rank == cards[2].rank == cards[3].rank) or
	    (cards[2].rank == cards[3].rank == cards[4].rank)):
	    # cards[2] will always be one of the trips
	    primaryRank = cards[2].rank
	    cards.removeRank(primaryRank)
	    return PokerRank.trips(primaryRank, cards)
	# Check for two pair	    
	# At this point we know we don't have trips, so can optimize some
	if (cards[0].rank == cards[1].rank):
	    if (cards[2].rank == cards[3].rank):
		return PokerRank.twoPair(cards[0].rank, cards[2].rank, cards[4:])
	    if (cards[3].rank == cards[4].rank):
		return PokerRank.twoPair(cards[0].rank, cards[3].rank, cards[2:3])
	elif ((cards[1].rank == cards[2].rank) and
	      (cards[3].rank == cards[4].rank)):
	    return PokerRank.twoPair(cards[1].rank, cards[3].rank, cards[0:1])
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
	    return PokerRank.pair(pairRank, cards)
	# Just a high card
	return PokerRank.highCard(cards[0].rank, cards[1:])
