#!/usr/bin/env python
"""Simulate chances of a five card board making flushes, pairs, etc."""

from optparse import OptionParser
from pyPoker.Hand import Board, Hand
from pyPoker.Cards import Suit, Rank
from pyPoker.Deck import Deck
import sys

def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "usage: %prog [<options>]"
    version = "%prog version 1.0"
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-n", "--numDeals", type="int", dest="numDeals",
                      default=1000,
                      help="number of deals to simulate (Default is 100)")
    parser.add_option("-p", "--showProgress", action="store_true",
                      dest="showProgress", default=False, help="show progress")
    (options, args) = parser.parse_args()

    print "Testing for %d deals" % options.numDeals

    possibleFlushes = 0

    flushCounts = [ 0, 0, 0, 0, 0, 0]
    rankCounts = [ 0, 0, 0, 0, 0]

    for deal in range(options.numDeals):
        deck = Deck()
        deck.shuffle()
        board = Board()
        deck.deal(board, 5)
        # Count flushes
        for suit in Suit.suits:
            count = board.suitCount(suit)
            flushCounts[count] += 1
        # Count pairs, trips and quads
        for rank in Rank.ranks:
            count = board.rankCount(rank)
            rankCounts[count] += 1
        if options.showProgress and (deal % 20 == 0):
            sys.stdout.write(".")
            sys.stdout.flush()

    if options.showProgress:
        print

    for index in range(len(flushCounts)):
        print "%d-flush ocurrances: %d" % (index,
                                           flushCounts[index])

    print "Board pairs: %d" % rankCounts[2]
    print "Board trips: %d" % rankCounts[3]
    print "Board quads: %d" % rankCounts[4]

if __name__ == "__main__":
    sys.exit(main())

