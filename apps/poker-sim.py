#!/usr/bin/env python
"""Poker game hand simulator."""

from optparse import OptionParser
import sys
import string
from pyPoker.PokerGame import PokerGame, HoldEmGame, FiveCardStudGame, FiveCardStudHiLoGame, SevenCardStudGame, SevenCardStudHiLoGame, OmahaGame, OmahaHiLoGame
from pyPoker.Hand import Hand, Board
from pyPoker.Hands import Hands
from pyPoker.Cards import Cards

######################################################################
#
# Callback for displaying each hand
#

def showHandCallback(game):
    print game.lastGameToString()

def showProgressCallback(game):
    sys.stdout.write(".")
    sys.stdout.flush()

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
    parser = OptionParser(usage)
    parser.add_option("-B", "--board", type="string", dest="board",
                      metavar="cards", help="specify the flop")
    parser.add_option("-g", "--game", type="string", dest="game",
                      default="holdem", help="game to simulate")
    parser.add_option("-H", "--hand", type="string", dest="hands",
                      metavar="cards", action="append", help="add a hand")
    parser.add_option("-n", "--numGames", type="int", dest="numGames",
                      default=100, help="number of games to simulate")
    parser.add_option("-N", "--numHands", type="int", dest="numHands",
                      default=10, help="number of hands in play")
    parser.add_option("-p", "--showProgress", action="store_true",
                      dest="showProgress", default=False, help="show progress")
    parser.add_option("-P", "--profile", type="string", dest="profile",
                      default=None, help="enable profiling")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      default=False, help="show results of each hand")

    (options, args) = parser.parse_args()

    game = {
        "holdem" : HoldEmGame,
        "5cardstud" : FiveCardStudGame,
        "fivecardstud" : FiveCardStudGame,
        "5cardstudhilo" : FiveCardStudHiLoGame,
        "fivecardstudhilo" : FiveCardStudHiLoGame,
        "7cardstud" : SevenCardStudGame,
        "sevencardstud" : SevenCardStudGame,
        "7cardstudhilo" : SevenCardStudHiLoGame,
        "sevencardstudhilo" : SevenCardStudHiLoGame,
        "omaha" : OmahaGame,
        "omahahilo" : OmahaHiLoGame,
        }

    if game.has_key(options.game):
        GameClass = game[options.game]
    else:
        print "Unknown game type \"%s\"" % options.game
        print "Known games are:"
        for name in game.keys():
            print "\t%s" % name
        sys.exit(1)

    maxHands = GameClass.getMaxHands()
    if options.numHands > maxHands:
        options.numHands = maxHands
        if options.verbose:
            print "Reducing number of hands to %d" % maxHands

    game = GameClass(numHands = options.numHands)
    HandClass = GameClass.getHandClass()

    if options.hands is not None:
        hands = Hands()
        for hand in options.hands:
            hands.addHand(HandClass.fromString(hand))
        game.addHands(hands)

    if options.board:
        game.setBoard(Board.fromString(options.board))

    if options.verbose:
        callback=showHandCallback

        print "Simulating %d games of %s" % (options.numGames,
					 GameClass.gameName)
        print "%d Hands" % game.getNumHands(),
        if game.hands:
            print ": %s" % game.hands
        else:
            print
        if game.board:
            print "Board: %s" % game.board
    elif options.showProgress:
        callback=showProgressCallback
    else:
        callback=None

    cmd="game.simulateGames(options.numGames, callback=callback)"

    if options.profile:
        import cProfile
        print "Profiling to file %s" % options.profile
        # Need to supply context here as run() will just use __main__
        cProfile.runctx(cmd, globals(), locals(), filename=options.profile)
    else:
        eval(cmd)

    if options.showProgress:
        print

    print game.statsToString()

if __name__ == "__main__":
    sys.exit(main())



