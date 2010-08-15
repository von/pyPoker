"""Class for representing a deck of playing cards."""

from PokerException import PokerException
from Cards import Cards, Card, Suit, Rank
from Hand import Hand
from Hands import Hands

######################################################################
#
# Exceptions
#

class NotEnoughCardsException(PokerException):
    """Tried to get more cards from a Deck than are in that Deck."""
    pass

class CardNotFoundException(PokerException):
    """Specified card not found in deck."""
    pass

######################################################################
#
# Deck Object
#

class Deck(Cards):
    # Number of cards in full deck
    numCards = 52

    def __init__(self, cards = None):
	"""Create a new deck of cards. Note that deck is not shuffled.  Deck
	will have standards 52 cards, unless arguments cards is not None, it
	should be a Cards object which the deck should contain."""
	if cards is None:
	    self.reset()
	else:
	    self.extend(cards)

    def reset(self):
	"""Reset to a fresh deck of 52 cards."""
	del self[:]
	for suit in Suit.suits:
	    for rank in Rank.ranks:
		self.append(Card((rank, suit)))

    def shuffle(self):
	"""Shuffle cards in deck. Note that this does not restore any dealt
	cards."""
	from random import shuffle
	shuffle(self)

    def deal(self, hands, numCards=1):
	"""Deal numCards to given hands. hands may be a single Hand or
	an array of Hands."""
	if numCards == 0:
	    return
	# Allow for a single hand
	if isinstance(hands, Hand):
	    hands = [ hands ]
	for card in range(numCards):
	    for hand in hands:
		hand.addCard(self.pop())

    def dealHands(self, hands):
        """Deal out full hands."""
	# Allow for a single hand
	if isinstance(hands, Hand):
	    h = hands
	    hands = Hands()
	    hands.addHand(h)
        while True:
            cardDealt = False
            for hand in hands:
		if not isinstance(hand, Hand):
		    raise InvalidHandTypeException("Bad hand type (%s)"
						   % hand.__class__)
                if len(hand) < hand.getMaxCards():
		    try:
			hand.addCard(self.pop())
		    except IndexError:
			raise NotEnoughCardsException
                    cardDealt = True
            if cardDealt == False:
                break

    def createHands(self, num, handClass=Hand):
	"""Create num complete hands and return. By default hands will be of
class Hand, but this can be overridden with handClass."""
	hands = []
	for hand in range(num):
	    hands.append(handClass())
	self.dealHands(hands)
	return hands

    def burn(self, numCards=1):
	"""Burn numCards cards."""
	for card in range(numCards):
	    self.pop()

    def findCard(self, card):
	"""Return index of given card in deck."""
	index = None
	for i in range(len(self)):
	    if self[i].eq(card):
		index = i
		break
	else:
	    raise CardNotFoundException("Card %s not found in deck." % card)
	return index

    def cardsInDeck(self, cards):
	"""Return True if all cards are in deck, False otherwise."""
	result = True
	for card in cards:
	    try:
		self.findCard(card)
	    except:
		result = False
		break
	return result

    def dealCard(self, hand, card):
	"""Deal a specific card to the given hand."""
	index = self.findCard(card)
	hand.addCard(self.pop(index))

    def removeCards(self, cards):
	"""Remove and discard the given card(s) from the deck."""
	if cards is None:
	    return
	if isinstance(cards, Card):
	    cards = [ cards ]
	for card in cards:
	    index = self.findCard(card)
	    self.pop(index)

    def copy(self):
	"""Return a copy of this Deck."""
	import copy
	return copy.copy(self)

