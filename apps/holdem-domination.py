#!/usr/bin/env python
"""What are our chances of our HoldEm hand being dominated?"""

from optparse import OptionParser
from pyPoker.Hand import HoldEmHand
from pyPoker.Cards import Card, Rank
from pyPoker.Deck import Deck
from pyPoker.PredefinedCards import *
from pyPoker.PokerRank import HoldEmStartingHandRank
import sys

######################################################################

def getVersionString():
    """Return our RCS/CVS version string."""
    import re
    revisionString = "$Revision$"
    match = re.match("\$Revision$", revisionString)
    if match is None:
        return "unknown"
    version = match.group(1)
    if version is None:
        return "unknown"
    return version

def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "usage: %prog [<options>]"
    version = "%prog version " + getVersionString()
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-n", "--numDeals", type="int", dest="numDeals",
                      default=1000,
                      help="number of deals to simulate (Default is 1000)")

    (options, args) = parser.parse_args()

    print "Testing for %d deals" % options.numDeals

    for rank1 in range(Eight, King):
        for rank2 in range(rank1 + 1, Ace):
            hand = HoldEmHand([Card((rank1, Clubs)),
                               Card((rank2, Clubs))])

            rank = HoldEmStartingHandRank(hand)

            # Build starting deck
            startingDeck = Deck()
            startingDeck.removeCards([hand[0], hand[1]])

            dominatedCount = 0

            for deal in range(options.numDeals):
                deck = startingDeck.copy()
                deck.shuffle()
                hands = deck.createHands(8, HoldEmHand)
                dominated = False
                for h in hands:
                    if ((h[0].rank == hand[0].rank) or
                        (h[0].rank == hand[1].rank) or
                        (h[1].rank == hand[0].rank) or
                        (h[1].rank == hand[1].rank)):
                        # We have domination
                        if (HoldEmStartingHandRank(h) > rank):
                            # Dealt hand is better
                            dominated = True
                if dominated:
                    dominatedCount += 1

            print "%s: %3.2f" % (hand, 100 * dominatedCount/options.numDeals)

if __name__ == "__main__":
    sys.exit(main())
