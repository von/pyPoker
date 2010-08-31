#!/usr/bin/env python
"""Structured Hand Analysis"""

from optparse import OptionParser
import sys
import string
import os
from pyPoker import HoldEm
from pyPoker.slanskyHands import SlanskyHand
from pyPoker.Hand import Board

######################################################################
#
# Callback for displaying each hand
#

def showHandCallback(game, result):
	output_game(result)

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

game = HoldEm.Game()

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

handNum = 1
while True:
    sectionName = "hand%d" % handNum
    hg = HoldEm.HandGenerator()
    hg.setName(sectionName)
    try:
	# Set raw to True so we don't try to parse %'s
	items = config.items(sectionName, raw=True)
    except:
	handNum -= 1
	break
    if options.verbose:
	print "Parsing hand %d..." % handNum
    for item in items:
	handstr, p = item
	percent = int(p.rstrip("%"))
	if (percent < 0) or (percent > 100):
	    print "Bad percentage (%s)" % p
	    continue
	print " %d%% " % percent,
	if handTypes.has_key(handstr):
	    hg.addHands(handTypes[handstr], percent)
	    print "%s hand generator" % handstr
	else:
	    hands = HoldEm.Hands()
	    for s in handstr.split():
		hands.addHandGroup(s)
	    hg.addHands(hands, percent)
	    print hands
#	else:
#	    print "Can't parse: %s = %s" % (attribute, value)
    game.addHandGenerator(hg)
    handNum += 1

if handNum == 0:
    print "No hands read from %s. Quitting." % configFileName
    sys.exit(0)

if options.verbose:
    print "Read %d hands" % handNum

try:
    boardStr = config.get("board", "cards")
except:
    pass
else:
    board = Board.fromString(boardStr)
    if options.verbose:
	print "Setting board: %s" % board
    game.setBoard(board)

if options.verbose:
    callback=showHandCallback
else:
    callback=None

if options.verbose:
    print "Running..."

stats = game.simulateGames(options.numGames, callback=callback)

output_stats(game, stats)

