#!/usr/bin/env python
######################################################################
#
# Structured Hand Analysis
#
# $Id$
#
######################################################################

from optparse import OptionParser
import sys
import string
import os
from pyPoker.PokerGame import HoldEmGame
from pyPoker.Hands import HoldEmHands
from pyPoker.HandGenerator import HoldEmHandGenerator
from pyPoker.slanskyHands import SlanskyHand
from pyPoker.Hand import Board

######################################################################
#
# Callback for displaying each hand
#

def showHandCallback(game):
	print game.lastGameToString()

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

game = HoldEmGame()

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
    hg = HoldEmHandGenerator()
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
	    hands = HoldEmHands()
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

game.simulateGames(options.numGames, callback=callback)

print game.statsToString()
