#!/usr/bin/env python
"""What are our chances of our HoldEm hand being dominated?"""

from optparse import OptionParser
from pyPoker import HoldEm
from pyPoker.Cards import Card, Rank
from pyPoker.Deck import Deck
from pyPoker.PredefinedCards import *
from pyPoker.HoldEmStartingHandRanker import HoldEmStartingHandRanker
import sys

def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "usage: %prog [<options>]"
    version = "%prog version 1.0"
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-n", "--numDeals", type="int", dest="numDeals",
                      default=1000,
                      help="number of deals to simulate (Default is 1000)")

    (options, args) = parser.parse_args()

    print "Testing for %d deals" % options.numDeals

    for rank1 in range(Eight, King):
        for rank2 in range(rank1 + 1, Ace):
            hand = HoldEm.Hand([Card((rank1, Clubs)),
                                Card((rank2, Clubs))])

            rank = HoldEmStartingHandRanker.rankHand(hand)

            # Build starting deck
            startingDeck = Deck()
            startingDeck.removeCards([hand[0], hand[1]])

            dominatedCount = 0

            for deal in range(options.numDeals):
                deck = startingDeck.copy()
                deck.shuffle()
                hands = deck.createHands(8, HoldEm.Hand)
                dominated = False
                for h in hands:
                    if ((h[0].rank == hand[0].rank) or
                        (h[0].rank == hand[1].rank) or
                        (h[1].rank == hand[0].rank) or
                        (h[1].rank == hand[1].rank)):
                        # We have domination
                        if (HoldEmStartingHandRanker.rankHand(h) > rank):
                            # Dealt hand is better
                            dominated = True
                if dominated:
                    dominatedCount += 1

            print "%s: %3.2f" % (hand, 100 * dominatedCount/options.numDeals)

if __name__ == "__main__":
    sys.exit(main())
