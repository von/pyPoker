#!/usr/bin/env python
"""Poker game hand simulator."""

from optparse import OptionParser
import sys
import string
from pyPoker import FiveCardStud, HoldEm, Omaha, SevenCardStud 
from pyPoker.Hand import Hand, Board
from pyPoker.Hands import Hands
from pyPoker.Cards import Cards

######################################################################
#
# Callback for displaying each hand
#

def showHandCallback(game, result):
    output_game(result)

def showProgressCallback(game, result):
    sys.stdout.write(".")
    sys.stdout.flush()


######################################################################
#
# Output routines

def output_stats(game, stats):
    hands = game.getHands()
    high_winners = stats.get_high_winners()
    low_winners = stats.get_low_winners()
    scoops = stats.get_scoops()
    number_of_games = stats.get_number_of_games()
    for index in range(game.getNumHands()):
        print "%2d:" % (index + 1),
        if index >= len(hands):
            print "XX " * game.getHandClass().getMaxCards(),
        else:
            print "%s " % hands[index],
        if high_winners is not None:
            print "High wins %4d (%3.0f%%)" % (
                high_winners[index],
                100.0 * high_winners[index] / number_of_games),
        if low_winners is not None:
            print " Low wins %4d (%3.0f%%)" % (
                low_winners[index],
                100.0 * low_winners[index] / number_of_games),
        if (low_winners is not None) and (high_winners is not None):
            print " Scoops: %d" % scoops[index],
        print


def output_game(result):
	if result.board is not None:
	    print "Board: %s " % result.board,
	if result.high_winners is not None:
	    print "High: %s " % result.winning_high_rank,
            print "(%s) " % (",".join(["%d:%s" % (hand + 1, result.hands[hand])
                                      for hand in result.high_winners])),
	if result.low_winners is not None:
	    s += "Low: %s " % result.winning_low_rank,
            print "(%s) " % (",".join(["%d:%s" % (hand + 1, result.hands[hand])
                                      for hand in result.low_winners])),
	if (result.high_winners is not None) and \
                (result.low_winners is not None):
            scoopers = filter(lambda i: i in result.low_winners,
                              result.high_winners)
            if len(scoopers) == 1:
		print "(Hand %d scoops)" % (scoopers[0]),
        print

######################################################################

def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "usage: %prog [<options>]"
    version = "%prog version 1.0"
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
    parser.add_option("-q", "--quiet", action="store_true",
                      dest="quiet", default=False, help="run quietly")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      default=False, help="show results of each hand")

    (options, args) = parser.parse_args()

    game = {
        "holdem" : HoldEm.Game,
        "5cardstud" : FiveCardStud.Game,
        "fivecardstud" : FiveCardStud.Game,
        "5cardstudhilo" : FiveCardStud.HiLoGame,
        "fivecardstudhilo" : FiveCardStud.HiLoGame,
        "7cardstud" : SevenCardStud.Game,
        "sevencardstud" : SevenCardStud.Game,
        "7cardstudhilo" : SevenCardStud.HiLoGame,
        "sevencardstudhilo" : SevenCardStud.HiLoGame,
        "omaha" : Omaha.Game,
        "omahahilo" : Omaha.HiLoGame,
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
        if options.verbose:
            print "Profiling to file %s" % options.profile
        # Need to supply context here as run() will just use __main__
        stats=cProfile.runctx(cmd, globals(), locals(), filename=options.profile)
    else:
        stats=eval(cmd)

    if options.showProgress:
        print

    if not options.quiet:
        output_stats(game, stats)

if __name__ == "__main__":
    sys.exit(main())



