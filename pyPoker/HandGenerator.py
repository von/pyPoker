######################################################################
#
# HandGenerator.py
#
# Class that generates a hand from a group of hands randomly.
#
# vwelch@ncsa.uiuc.edu
# $Id$
#
######################################################################

from PokerException import PokerException
from Hand import Hand, HoldEmHand
from Deck import Deck

######################################################################
#
# Exceptions
#

class HandGenerationException(PokerException):
    """Could not generate specified hand from deck due to lack of cards."""
    pass

######################################################################
#
# HandGenerator class
#

class HandGenerator:
    """Given an array of possible hands, this class generates one of these hands randomly when requested."""
    def __init__(self, handType, hands=None, deck=None, name = None):
	"""handType should be a class for the type of hands to be generated.

	hands should be an array of Cards representing valid hands that
	can be generated.

	deck is optional. If not None, then it represents a deck that the
	generated hands should be drawn from.
	"""
	self.handType = handType
	self.hands = []
	if hands:
	    self.hands.append((100, hands))
	    self.totalPercentage = 100
	else:
	    self.totalPercentage = 0
	self.deck = deck
	self.name = name

    def generateHand(self, deck=None):
	"""Generate a hand.

	If deck is provided, then it is a Deck from which hand is drawn."""
	from random import choice, shuffle
	hands = self._pickHands()
	if deck is None:
	    deck = self.deck
	if deck is None:
	    # No deck to constrian choices, just pick a hand at random
	    hand = self.handType(cards = choice(hands))
	else:
	    # We need to ensure our choice can be drawn from the deck
	    # Put hands in random order and try in sequence
	    shuffle(hands)
	    for h in hands:
		if deck.cardsInDeck(h):
		    deck.removeCards(h)
		    hand = self.handType(cards = h)
		    break
	    else:
		raise HandGenerationException("Couldn't find hand in deck.")
	return hand

    def addHands(self, hands, percentage=100):
	if (percentage < 0) or (percentage > 100):
	    raise InvalidArgument("Percentage (%d) out of range." % percentage)
	if self.totalPercentage + percentage > 100:
	    raise ValueError("Percent total greater than 100")
	self.hands.append((percentage, hands))
	self.totalPercentage += percentage

    def _pickHands(self):
	from random import randint
	# check hands and make sure percentage adds up to 100
	if self.totalPercentage != 100:
	    raise HandGenerationException("Bad total percentage for hand (%d%%)" % self.totalPercentage)
	rand = randint(1,100)
	total = 0
	for h in self.hands:
	    (percent, hands) = h
	    if total + percent >= rand:
		return hands
	    total += percent
	# Should never get here
	raise PokerInternalException("Didn't match a hand")
	
    def __str__(self):
	if self.name:
	    return self.name
	else:
	    return "%s" % self.__class__
    
    def dump(self):
	for h in self.hands:
	    per, hand = h
	    print "%d%%: %s" % (per, hand)

class HoldEmHandGenerator(HandGenerator):
    def __init__(self, hands = None, deck = None, name = None):
	HandGenerator.__init__(self, HoldEmHand,
			       hands=hands, deck=deck,
			       name=name)
