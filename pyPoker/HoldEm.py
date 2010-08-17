"""Texas HoldEm classes"""

from Cards import Card, Rank, Suit
from Hand import CommunityCardHand, FiveCardBoard
from PokerException import PokerException
from PokerGame import CommunityCardPokerGame
from PokerRank import PokerRank
from Ranker import RankerBase
from Utils import assertInstance

# Import following using full names to avoid internal conflicts
# with classes having same names
import pyPoker.HandGenerator
import pyPoker.Hands


class Hand(CommunityCardHand):
    """A Texas HoldEM hand (2 hole cards with 5-card board)"""
    maxCards = 2
    boardClass = FiveCardBoard

    def __init__(self, cards = None, board = None):
	"""Create a Texas Hold'Em hand.
	cards should be none or an array of up to two cards.
	board should be a Board object."""
	CommunityCardHand.__init__(self, cards, board = board)


class Hands(pyPoker.Hands.Hands):
    """Class for creating and containing groups of TexasHoldEm hands.

    Allows for each creation of grounds of hands such as K9-suited representing
    all possible variables of a suited King and Nine."""
    handType = Hand

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
	    self.append(Hand([Card((rank1, suit)),
                              Card((rank2, suit))]))

    def addUnsuitedHands(self, rank1, rank2):
	for suit1 in Suit.suits:
	    for suit2 in Suit.suits:
		if suit1 == suit2:
		    continue
		self.append(Hand([Card((rank1, suit1)),
                                  Card((rank2, suit2))]))

    def addAllHands(self, rank1, rank2):
	for suit1 in Suit.suits:
	    for suit2 in Suit.suits:
		self.append(Hand([Card((rank1, suit1)),
                                  Card((rank2, suit2))]))

    def addPair(self, rank):
	for index1 in range(len(Suit.suits) - 1):
	    for index2 in range(index1 + 1, len(Suit.suits)):
		suit1 = Suit.suits[index1]
		suit2 = Suit.suits[index2]
		self.append(Hand([Card((rank, suit1)),
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

class HandGenerator(pyPoker.HandGenerator.HandGenerator):
    handClass = Hand

class Game(CommunityCardPokerGame):
    handClass = Hand
    gameName = "Texas Hold'em"

class StartingHandRanker(RankerBase):
    """Rank starting HoldEm hands"""
    
    @classmethod
    def rankHand(cls, hand):
        """Rank a hold'em hand (pair or high card)."""
        if hand[0].rank == hand[1].rank:
            return PokerRank.pair(hand[0].rank, kickers=None)
        if hand[0].rank > hand[1].rank:
            return PokerRank.highCard(hand[0].rank, hand[1:])
        else:
            return PokerRank.highCard(hand[1].rank, hand[:1])

######################################################################

class InvalidHandTypeException(PokerException):
    """An invalid hand description was passed as an input."""
    pass
