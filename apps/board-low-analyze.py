#!/usr/bin/env python
######################################################################
#
# Simulate chances five card board making eight low
#
# $Id$
#
######################################################################

from optparse import OptionParser
from pyPoker.Hand import Board
from pyPoker.Deck import Deck
import sys

######################################################################

def printStat(name, value):
    print "%-30s %5d (%5.2f%%)" % (name.capitalize() + ":",
				    value,
				    100.0 * value / options.numDeals)

######################################################################

usage = "usage: %prog [<options>]"
parser = OptionParser(usage)
parser.add_option("-n", "--numDeals", type="int", dest="numDeals",
		  default=1000, help="number of deals to simulate (Default is 100)")
parser.add_option("-p", "--showProgress", action="store_true",
		  dest="showProgress", default=False, help="show progress")
(options, args) = parser.parse_args()

######################################################################

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

printStat("eight-low possible", lowPossible)
printStat("flopped low", floppedLow)
printStat("flopped low draw", lowDraw)
printStat("completed draw", lowDrawCompleted)
printStat("backdoor low", backdoorLow)

sys.exit(0)
