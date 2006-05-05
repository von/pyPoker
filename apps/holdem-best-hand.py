#!/usr/bin/env python
######################################################################
#
# Do I have the best Texas hold'em hand pre-flop?
#
# $Id$
#
######################################################################

from optparse import OptionParser
import sys
import string
from pyPoker.Cards import Card, Cards, Suit, Rank
from pyPoker.Hand import HoldEmHand
from pyPoker.Deck import Deck
from pyPoker.PokerRank import HoldEmStartingHandRank

######################################################################

def printHeader():
    print
    print " Hand",
    for i in range(options.numHands):
	print " %3d " % (i+1),
    print

def evaluateHand(hand):
    handRank = HoldEmStartingHandRank(hand)
    betterThan = [ 0 ] * options.numHands
    for deal in range(options.numDeals):
	deck = Deck()
	deck.removeCards(hand)
	deck.shuffle()
	hands = []
	for h in range(options.numHands):
	    hands.append(HoldEmHand())
	deck.dealHands(hands)
	for h in range(options.numHands):
	    rank = HoldEmStartingHandRank(hands[h])
	    if handRank > rank:
		betterThan[h] += 1
	    else:
		break
    return betterThan

######################################################################

usage = "usage: %prog [<options>]"
parser = OptionParser(usage)
parser.add_option("-n", "--numDeals", type="int", dest="numDeals",
		  default=1000, help="number of deals to simulate (Default is 100)")
parser.add_option("-N", "--numHands", type="int", dest="numHands",
		  default=8, help="number of hands to compare against (Default is 8)")

(options, args) = parser.parse_args()

print "Testing up to %d opposing hands, %d simulated deals" % (options.numHands,
							       options.numDeals)

count = 0
printHeader()
for topRank in Rank.ranks:
    if count > 10:
	printHeader()
	count = 0
    for lowRank in range(2, topRank + 1):
	# We'll do pairs last
	if topRank == lowRank:
	    continue
	cards = Cards([Card((topRank, Suit.CLUBS)),
		       Card((lowRank, Suit.SPADE))])
	hand = HoldEmHand(cards)
	betterThan = evaluateHand(hand)
	print hand,
	for h in range(options.numHands):
	    print " %3d%%" % ((100 * betterThan[h]) / options.numDeals),
	print
	count += 1

# Now do pairs
printHeader()
for rank in Rank.ranks:
    cards = Cards([Card((rank, Suit.CLUBS)),
		   Card((rank, Suit.SPADE))])
    hand = HoldEmHand(cards)
    betterThan = evaluateHand(hand)
    print hand,
    for h in range(options.numHands):
	print " %3d%%" % ((100 * betterThan[h]) / options.numDeals),
    print

sys.exit(0)
