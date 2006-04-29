######################################################################
#
# HandGroup
# 
# Class for generating groups of hands.
#
# $Id$
######################################################################

from PokerException import PokerException
from Hand import Hand
from Cards import Card, Suit, Rank

######################################################################

class InvalidHandTypeException(PokerException):
    """An invalid hand description was passed as an input."""
    pass


SUITED = True
UNSUITED = False

class HoldEmHands(Hands):
    def __init__(self, *groups):
	self.addHandGroups(*groups)

    def addHandGroups(self, *groups):
	for group in groups:
	    if isinstance(group, list):
		self.addHandGroups(*group)
	    else:
		self.addHandGroup(group)

    def addHandGroup(self, group):
	if isinstance(group, str):
	    rank1, rank2, suited = self._parseHandString(group)
	else:
	    raise BadHandGroupException("Invalid type %s" % group.__class__)
	if rank1 == rank2:
	    self.addPair(rank1)
	elif suited is True:
	    self.addSuitedHands(rank1, rank2)
	elif suited is False:
	    self.addUnsuitedHands(rank1, rank2)
	else:
	    self.addAllHands(rank1, rank2)

    def _parseHandString(handStr):
	if len(handStr) == 2:
	    rank1 = Rank.fromChar(handStr[0])
	    rank2 = Rank.fromChar(handStr[1])
	    suited = None
	elif len(handStr) == 3:
	    rank1 = Rank.fromChar(handStr[0])
	    rank2 = Rank.fromChar(handStr[1])
	    suitedChar = handStr[2]
	    if suitedChar == 's':
		suited = True
	    else:
		raise BadHandGroupException("Invalid suited character \"%s\"" %
					    suitedChar)
	else:
	    raise BadHandGroupException("Invalid hand string \"%s\"" % handStr)
	return rank1, rank2, suited

    _parseHandString = staticmethod(_parseHandString)

    def addSuitedHands(self, rank1, rank2):
	for suit in Suit.suits:
	    self.append(Cards([Card((rank1, suit)), Card((rank2, suit))]))

    def addUnsuitedHands(self, rank1, rank2):
	for suit1 in Suit.suits:
	    for suit2 in Suit.suits:
		if suit1 == suit2:
		    continue
		self.append(Cards([Card((rank1, suit1)), Card((rank2, suit2))]))

    def addAllHands(self, rank1, rank2):
	for suit1 in Suit.suits:
	    for suit2 in Suit.suits:
		self.append(Cards([Card((rank1, suit1)), Card((rank2, suit2))]))

    def addPair(self, rank):
	for suit1 in Suit.suits:
	    # XXX Fix this
	    for suit2 in range(suit1 + 1, Suit.SPADES + 1):
		self.append(Cards([Card((rank, suit1)), Card((rank, suit2))]))

    def addSuitedCardXHands(self, rank1):
	"""Added all hands composed of rank and 2 through 9."""
	for rank2 in range(2,SUIT.TEN):
	    self.addSuitedHands(rank1, rank2)

    def addSuitedAceXHands(self):
	"""Add suited A2 through A9."""
	self.addSuitedCardXHands(SUIT.ACE)

    def addSuitedKingXHands(self):
	"""Add suited K2 through K9."""
	self.addSuitedCardXHands(SUIT.KING)
