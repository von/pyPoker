"""Class for generating groups of hands."""

from Hand import Hand

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
