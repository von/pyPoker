#!/usr/bin/env python
"""Figure out average point value of random omaha8 hands."""

from optparse import OptionParser
import sys
from pyPoker import Omaha
from pyPoker.Deck import Deck

######################################################################

def percent(num, total):
    if (num == 0) and (total == 0):
        # Punt instead of croaking
        return 0.0
    return 100.0 * num / total

######################################################################

def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "usage: %prog [<options>] Card1 Card2 Card3 Card4"
    version = "%prog version 1.0"
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-n", "--numDeals", type="int", dest="numDeals",
                      default=1000,
                      help="number of deals to simulate (Default is 100)")
    parser.add_option("-N", "--numHands", type="int", dest="numHands",
                      default=8, help="number of Hands (Default is 8)")
    parser.add_option("-p", "--showProgress", action="store_true",
                      dest="showProgress", default=False, help="show progress")
    (options, args) = parser.parse_args()

    total = 0
    pointOpeningHands = 0
    pointRaisingHands = 0
    pointReraisingHands = 0
    maxPointOpeners = 0
    openingHands = 0

    for deal in xrange(options.numDeals):
        deck = Deck()
        deck.shuffle()
        hands = deck.createHands(options.numHands, handClass = Omaha.Hand)
        dealOpeners = 0
        for h in hands:
            value = h.pointValue()
            total += value
            if value > 25:
                dealOpeners += 1
                pointOpeningHands += 1
            if value > 40:
                pointRaisingHands += 1
            if value > 50:
                pointReraisingHands += 1
            if h.openingHand():
                openingHands += 1
        if dealOpeners > maxPointOpeners:
            maxPointOpeners = dealOpeners
        # Update progress if so requested
        if options.showProgress and (deal % 20 == 0):
            sys.stdout.write(".")
            sys.stdout.flush()

    if options.showProgress:
        print

    totalHands = options.numDeals * options.numHands

    avg = total/totalHands

    print "Average point value: %d" % avg
    print "\tOpeners: %5.2f%% Raisers: %5.2f%% Reraisers: %5.2f%%" % (
        percent(pointOpeningHands, totalHands),
        percent(pointRaisingHands, totalHands),
        percent(pointReraisingHands, totalHands))
    print "\tOpeners in a deal: Average %4.1f Max %d" % (
        1.0 * pointOpeningHands / options.numDeals,
        maxPointOpeners)
    print "Opening Hands by Krieger method: %5.2f%%" % percent(openingHands,
                                                               totalHands)

if __name__ == "__main__":
    sys.exit(main())


