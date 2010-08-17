#!/usr/bin/env python
"""Do I have the best Texas hold'em hand pre-flop?"""

from optparse import OptionParser
import sys
import string
from pyPoker.Cards import Card, Cards, Suit, Rank
from pyPoker import HoldEm
from pyPoker.HoldEmStartingHandRanker import HoldEmStartingHandRanker
from pyPoker.Deck import Deck

######################################################################

def printHeader(numHands):
    print
    print " Hand",
    for i in range(numHands):
	print " %3d " % (i+1),
    print

def evaluateHand(hand, numDeals, numHands):
    handRank = HoldEmStartingHandRanker.rankHand(hand)
    betterThan = [ 0 ] * numHands
    for deal in range(numDeals):
	deck = Deck()
	deck.removeCards(hand)
	deck.shuffle()
	hands = []
	for h in range(numHands):
	    hands.append(HoldEm.Hand())
	deck.dealHands(hands)
	for h in range(numHands):
	    rank = HoldEmStartingHandRanker.rankHand(hands[h])
	    if handRank > rank:
		betterThan[h] += 1
	    else:
		break
    return betterThan

######################################################################

def main(argv=None):
    if argv is None:
        argv = sys.argv

        usage = "usage: %prog [<options>]"
        version = "%prog version 1.0"
        parser = OptionParser(usage=usage, version=version)
        parser.add_option("-n", "--numDeals", type="int", dest="numDeals",
                          default=1000,
                          help="number of deals to simulate (Default is 100)")
        parser.add_option("-N", "--numHands", type="int", dest="numHands",
                          default=8,
                          help="number of hands to compare against (Default is 8)")

        (options, args) = parser.parse_args()

        print "Testing up to %d opposing hands, %d simulated deals" % (options.numHands,
                                                                       options.numDeals)

        count = 0
        printHeader(options.numHands)
        for topRank in Rank.ranks:
            if count > 10:
                printHeader(options.numHands)
                count = 0
        for lowRank in range(2, topRank + 1):
            # We'll do pairs last
            if topRank == lowRank:
                continue
            cards = Cards([Card((topRank, Suit.CLUBS)),
                           Card((lowRank, Suit.SPADE))])
            hand = HoldEm.Hand(cards)
            betterThan = evaluateHand(hand, options.numDeals, options.numHands)
            print hand,
            for h in range(options.numHands):
                print " %3d%%" % ((100 * betterThan[h]) / options.numDeals),
            print
            count += 1

    # Now do pairs
    printHeader(options.numHands)
    for rank in Rank.ranks:
        cards = Cards([Card((rank, Suit.CLUBS)),
                       Card((rank, Suit.SPADE))])
        hand = HoldEm.Hand(cards)
        betterThan = evaluateHand(hand, options.numDeals, options.numHands)
        print hand,
        for h in range(options.numHands):
            print " %3d%%" % ((100 * betterThan[h]) / options.numDeals),
        print

if __name__ == "__main__":
    sys.exit(main())

