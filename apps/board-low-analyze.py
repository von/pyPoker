#!/usr/bin/env python
"""Simulate chances five card board making eight low."""

from optparse import OptionParser
from pyPoker.Hand import Board
from pyPoker.Deck import Deck
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
                      help="number of deals to simulate (Default is 100)")
    parser.add_option("-p", "--showProgress", action="store_true",
                      dest="showProgress", default=False, help="show progress")
    (options, args) = parser.parse_args()

    print "Testing for %d deals" % options.numDeals

    lowDraw = 0
    lowDrawCompleted = 0
    floppedLow = 0
    lowPossible = 0
    backdoorLow = 0

    for deal in range(options.numDeals):
        deck = Deck()
        deck.shuffle()
        board = Board()
        # Deal out flop and count low cards
        deck.deal(board, 3)
        flopLowCount = board.countEightOrLower()
        if flopLowCount == 2:
            lowDraw += 1
        # Finish dealing turn and river
        deck.deal(board, 2)
        # Analyze
        lowCount = board.countEightOrLower()
        if lowCount > 2:
            lowPossible += 1
            if flopLowCount == 3:
                # Flopped a low
                floppedLow += 1
            elif flopLowCount == 2:
                # Completed a draw
                lowDrawCompleted += 1
            else:
                # Backdoor low
                backdoorLow += 1
        # Update progress if so requested
        if options.showProgress and (deal % 20 == 0):
            sys.stdout.write(".")
            sys.stdout.flush()

    if options.showProgress:
        print

    statStr = lambda name, value: "%-30s %5d (%5.2f%%)" % (name.capitalize() + ":", value, 100.0 * value / options.numDeals)

    print statStr("eight-low possible", lowPossible)
    print statStr("flopped low", floppedLow)
    print statStr("flopped low draw", lowDraw)
    print statStr("completed draw", lowDrawCompleted)
    print statStr("backdoor low", backdoorLow)

if __name__ == "__main__":
    sys.exit(main())
