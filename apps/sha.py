#!/usr/bin/env python
"""Structured Hand Analysis"""

from optparse import OptionParser
import sys
import string
import os
from pyPoker import HoldEm
from pyPoker.slanskyHands import SlanskyHand
from pyPoker.Hand import Board
from pyPoker.Hands import Hands

######################################################################
#
# Callback for displaying each hand
#

def showHandCallback(simulator, result):
    output_game(result)
    

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

usage = "usage: %prog [<options>] <input file>"
parser = OptionParser(usage)
parser.add_option("-n", "--numGames", type="int", dest="numGames",
		  default=100, help="number of games to simulate")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
		  default=False, help="show results of each hand")
(options, args) = parser.parse_args()

######################################################################
#
# Configuration
#

import ConfigParser

try:
    configFileName = args.pop()
except:
    parser.print_help()
    sys.exit(1)

try:
    os.stat(configFileName)
except OSError, e:
    print "Could not read configuration file: %s" % e
    sys.exit(1)

if options.verbose:
    print "Reading hands from %s..." % configFileName

config = ConfigParser.SafeConfigParser()
try:
    config.read(configFileName)
except Exception, e:
    print "Error parsing configuration file: %s" % e
    sys.exit(1)

handTypes = {}
handTypes.update(SlanskyHand)

predefined_hands = Hands()
while True:
    hand_num = len(predefined_hands) + 1
    sectionName = "hand%d" % hand_num
    try:
	# Set raw to True so we don't try to parse %'s
	items = config.items(sectionName, raw=True)
    except:
	break
    if options.verbose:
	print "Parsing hand %d..." % hand_num
    hg = HoldEm.HandGenerator()
    hg.setName(sectionName)
    for item in items:
	handstr, p = item
	percent = int(p.rstrip("%"))
	if (percent < 0) or (percent > 100):
	    print "Bad percentage (%s)" % p
	    continue
	if options.verbose:
		print " %d%% " % percent,
	if handTypes.has_key(handstr):
	    hg.addHands(handTypes[handstr], percent)
	    if options.verbose:
		    print "%s hand generator" % handstr
	else:
	    hands = HoldEm.Hands()
	    for s in handstr.split():
		hands.addHandGroup(s)
	    hg.addHands(hands, percent)
	    if options.verbose:
		    print hands
#	else:
#	    print "Can't parse: %s = %s" % (attribute, value)
    predefined_hands.append(hg)

if len(predefined_hands) == 0:
	print "No hands read from %s. Quitting." % configFileName
	sys.exit(0)

if options.verbose:
    print "Read %d hands" % len(predefined_hands)

predefined_board = None
try:
    boardStr = config.get("board", "cards")
except:
    pass
else:
    predefined_boardboard = Board.fromString(boardStr)
    if options.verbose:
	print "Setting board: %s" % board
    game.setBoard(board)

if options.verbose:
    callback=showHandCallback
else:
    callback=None

if options.verbose:
    print "Running..."

simulator = HoldEm.Simulator(predefined_hands=predefined_hands,
			     predefined_board=predefined_board)

stats = simulator.simulate_games(number_of_games=options.numGames,
				 callback=callback)

output_stats(simulation=simulator,
	     stats=stats)

