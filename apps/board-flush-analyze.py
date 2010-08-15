#!/usr/bin/env python
"""Simulate chances five card board making flushes."""

from optparse import OptionParser
from pyPoker.Hand import Board
from pyPoker.Cards import Card, Suit, Rank
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
    parser.add_option("-s", "--suitedCards", type="int", dest="suitedCards",
                      default=2,
                      help="number of suited cards in hand (default is 2)")
    (options, args) = parser.parse_args()


    print "Testing for %d deals, %d suited cards in hand" % (options.numDeals,
                                                             options.suitedCards)

    # Two-dimensional array. First dimension is number of cards of given suit
    # on flop, second dimension is number of cards of given suit on full board
    count = []
    for index in range(4):
        count.append([0] * 6)

    # The suit we care about
    suit = Suit(Suit.CLUBS)

    # Build starting deck
    startingDeck = Deck()
    for index in range(options.suitedCards):
        startingDeck.removeCards(Card((Rank(Rank.ranks[index]), suit)))

    madeFlushes = [0] * 4

    for deal in range(options.numDeals):
        deck = startingDeck.copy()
        deck.shuffle()
        board = Board()
        # Deal out and save flop
        deck.deal(board, 3)
        flop = board.copy()
        # Deal turn and river
        deck.deal(board, 2)
        # Find highest number of cards of same suit
        flushCount = 0
        flopCount = flop.suitCount(suit)
        boardCount = board.suitCount(suit)
        count[flopCount][boardCount] += 1
        if (options.suitedCards + boardCount) > 4:
            madeFlushes[flopCount] += 1
        # Update progress if so requested
        if options.showProgress and (deal % 20 == 0):
            sys.stdout.write(".")
            sys.stdout.flush()

    if options.showProgress:
        print

    colwidth = 6

    for col in ["Flopped", "Occur", "Final", "0", "1", "2", "3", "4", "5", "Flushes"]:
        print col.center(colwidth),
    print

    for index in range(len(count)):
        array = count[index]
        total = reduce(lambda a,b: a + b, array)
        print str(index).rjust(colwidth),
        print str(total).rjust(colwidth),
        print " ".ljust(colwidth),
        if total > 0:
            for subindex in range(len(array)):
                if ((subindex < index) or
                    (subindex > index + 3)):
                    print " ".ljust(colwidth),
                else:
                    s = "%3.0f%%" % (100.0 * array[subindex]/total)
                    print s.rjust(colwidth),
            s = "%3.0f%%" % (100.0 * madeFlushes[index]/total)
            print s,
        print

    totalFlushes = reduce(lambda a,b: a + b, madeFlushes)
    print "Total made flushes: %d (%3.0f%%)" % (totalFlushes,
                                                100.0 * totalFlushes / options.numDeals)

if __name__ == "__main__":
    sys.exit(main())
