"""Class for generating groups of hands."""

from PokerException import PokerException
from Hand import Hand, HoldEmHand
from Cards import Card, Suit, Rank
from Utils import assertInstance

######################################################################

class InvalidHandTypeException(PokerException):
    """An invalid hand description was passed as an input."""
    pass

######################################################################
#
# Hands
#

class Hands(list):
    """An array of hands."""
    handType = Hand

    def __init__(self, hands = None):
	"""Create an array of hands. Argument should be an array of Hand objects."""
	if hands:
	    self.addHands(hands)

    def addHand(self, hand):
	self.append(hand)

    def addHandFromString(self, string):
	self.append(Hand.fromString(string))

    def addHands(self, hands):
	for hand in hands:
	    self.addHand(hand)

    def addHandsFromStrings(self, strings):
	for string in strings:
	    self.addHandFromString(string)

    def __str__(self):
	s =""
	for hand in self:
	    s += str(hand) + ", "
	return s.rstrip(', ')

    def containsHand(self, hand):
	"""Does hands object contain the given hand?"""
	for h in self:
	    if hand.eq(h):
		return True
	return False

######################################################################

class HoldEmHands(Hands):
    handType = HoldEmHand

    def addHandGroup(self, string):
	"""Add a group of hands as described by string. string should have one
	of two forms:
	K4 - all unsuited combinations of K4.
	K4s - all suited combinations of K4.
	"""
	assertInstance(string, str)
	if len(string) == 2:
	    rank1 = Rank.fromString(string[0])
	    rank2 = Rank.fromString(string[1])
	    suited = False
	elif len(string) == 3:
	    rank1 = Rank.fromString(string[0])
	    rank2 = Rank.fromString(string[1])
	    suitedChar = string[2]
	    if suitedChar == 's':
		suited = True
	    else:
		raise InvalidHandTypeException("Invalid suited character \"%s\"" %
					    suitedChar)
	else:
	    raise InvalidHandTypeException("Invalid hand string \"%s\"" % 
					   string)
	if rank1 == rank2:
	    self.addPair(rank1)
	elif suited:
	    self.addSuitedHands(rank1, rank2)
	else:
	    self.addUnsuitedHands(rank1, rank2)

    @classmethod
    def fromGroups(cls, *strings):
	hands = cls()
	for string in strings:
	    hands.addHandGroup(string)
	return hands

    def addSuitedHands(self, rank1, rank2):
	for suit in Suit.suits:
	    self.append(HoldEmHand([Card((rank1, suit)),
				    Card((rank2, suit))]))

    def addUnsuitedHands(self, rank1, rank2):
	for suit1 in Suit.suits:
	    for suit2 in Suit.suits:
		if suit1 == suit2:
		    continue
		self.append(HoldEmHand([Card((rank1, suit1)),
					Card((rank2, suit2))]))

    def addAllHands(self, rank1, rank2):
	for suit1 in Suit.suits:
	    for suit2 in Suit.suits:
		self.append(HoldEmHand([Card((rank1, suit1)),
					Card((rank2, suit2))]))

    def addPair(self, rank):
	for index1 in range(len(Suit.suits) - 1):
	    for index2 in range(index1 + 1, len(Suit.suits)):
		suit1 = Suit.suits[index1]
		suit2 = Suit.suits[index2]
		self.append(HoldEmHand([Card((rank, suit1)),
					Card((rank, suit2))]))

    def addSuitedCardXHands(self, rank1):
	"""Added all hands composed of rank and 2 through 9."""
	for rank2 in range(2,Rank.TEN):
	    self.addSuitedHands(rank1, rank2)

    def addSuitedAceXHands(self):
	"""Add suited A2 through A9."""
	self.addSuitedCardXHands(Rank.ACE)

    def addSuitedKingXHands(self):
	"""Add suited K2 through K9."""
	self.addSuitedCardXHands(Rank.KING)
