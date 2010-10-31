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

def showHandCallback(simulator, result):
    output_game(result)

def showProgressCallback(simulator, result):
    sys.stdout.write(".")
    sys.stdout.flush()


######################################################################
#
# Output routines

def output_stats(simulation, stats):
    high_winners = stats.get_high_winners()
    low_winners = stats.get_low_winners()
    scoops = stats.get_scoops()
    number_of_games = stats.get_number_of_games()
    predefined_hands = simulation.get_predefined_hands()
    for index in range(stats.get_number_of_hands()):
        print "%2d:" % (index + 1),
        if index >= len(predefined_hands):
            print "XX " * simulation.HandClass.getMaxCards(),
        else:
            print "%s " % predefined_hands[index],
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
        "holdem" : HoldEm.Simulator,
        "5cardstud" : FiveCardStud.Simulator,
        "fivecardstud" : FiveCardStud.Simulator,
        "5cardstudhilo" : FiveCardStud.HiLoSimulator,
        "fivecardstudhilo" : FiveCardStud.HiLoSimulator,
        "7cardstud" : SevenCardStud.Simulator,
        "sevencardstud" : SevenCardStud.Simulator,
        "7cardstudhilo" : SevenCardStud.HiLoSimulator,
        "sevencardstudhilo" : SevenCardStud.HiLoSimulator,
        "omaha" : Omaha.Simulator,
        "omahahilo" : Omaha.HiLoSimulator,
        }

    if game.has_key(options.game):
        SimulatorClass = game[options.game]
    else:
        print "Unknown game type \"%s\"" % options.game
        print "Known games are:"
        for name in game.keys():
            print "\t%s" % name
        sys.exit(1)

    maxHands = SimulatorClass.getMaxHands()
    if options.numHands > maxHands:
        options.numHands = maxHands
        if options.verbose:
            print "Reducing number of hands to %d" % maxHands

    HandClass = SimulatorClass.HandClass

    hands = Hands()
    if options.hands is not None:
        for hand in options.hands:
            hands.addHand(HandClass.fromString(hand))

    if options.board:
        board = Board.fromString(options.board)
    else:
        board = None

    if options.verbose:
        callback=showHandCallback

        print "Simulating %d games of %s" % (options.numGames,
                                             SimulatorClass.GAME_NAME)
        print "%d Hands" % options.numHands
        if hands is not None:
            print ": %s" % hands
        else:
            print
        if board is not None:
            print "Board: %s" % board
    elif options.showProgress:
        callback=showProgressCallback
    else:
        callback=None

    simulator = SimulatorClass(number_of_hands = options.numHands,
                               predefined_hands = hands,
                               predefined_board = board)

    cmd="simulator.simulate_games(number_of_games=options.numGames, callback=callback)"

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
        output_stats(simulation=simulator,
                     stats=stats)

if __name__ == "__main__":
    sys.exit(main())



