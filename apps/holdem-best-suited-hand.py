#!/usr/bin/env python
######################################################################
#
# Determine your chance of having the best suited HoldEm hand with
# a given high card.
#
# $Id$
#
######################################################################

from optparse import OptionParser
from pyPoker.Hand import HoldEmHand
from pyPoker.Cards import Card, Suit, Rank
from pyPoker.Deck import Deck
import sys

######################################################################

def percent(num, total):
    if (num == 0) and (total == 0):
        # Punt instead of croaking
        return 0.0
    return 100.0 * num / total

######################################################################

usage = "usage: %prog [<options>]"
parser = OptionParser(usage)
parser.add_option("-n", "--numDeals", type="int", dest="numDeals",
		  default=1000, help="number of deals to simulate (Default is 100)")
parser.add_option("-N", "--numHands", type="int", dest="numHands",
		  default=8, help="number of Hands (Default is 8)")
parser.add_option("-p", "--showProgress", action="store_true",
		  dest="showProgress", default=False, help="show progress")

(options, args) = parser.parse_args()

######################################################################

print "Testing for %d deals against %d hands" % (options.numDeals,
						 options.numHands)

print "Rank\tOther\tBetter"

suit = Suit(Suit.CLUBS)

for rank in range(Rank.FIVE, Rank.ACE):
    startingDeck = Deck()
    hand = HoldEmHand()
    startingDeck.dealCard(hand, Card((Rank(rank), suit)))
    startingDeck.dealCard(hand, Card((Rank(Rank.TWO), suit)))
    otherSuitedHands = 0
    betterSuitedHands = 0
    for i in xrange(options.numDeals):
	deck = startingDeck.copy()
	deck.shuffle()
	hands = deck.createHands(options.numHands, handClass=HoldEmHand)
	otherSuitedHand = 0
	betterSuitedHand = 0
	for h in hands:
	    if h.suitCount(suit) == 2:
		otherSuitedHand = 1
		if (h[0].rank > rank) or (h[1].rank > rank):
		    betterSuitedHand = 1
	otherSuitedHands += otherSuitedHand
	betterSuitedHands += betterSuitedHand
    print "%s\t%5.2f%%\t%5.2f%%" % (Rank(rank).longString(),
				    percent(otherSuitedHands, options.numDeals),
				    percent(betterSuitedHands, options.numDeals))

sys.exit(0)