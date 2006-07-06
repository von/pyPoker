#!/usr/bin/env python
######################################################################
#
# Poker game hand simulator
#
# $Id$
#
######################################################################

from optparse import OptionParser
import sys
import string
from pyPoker.PokerGame import PokerGame, HoldEmGame, FiveCardStudHiLoGame, OmahaGame, OmahaHiLoGame
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
#
# Types for Game and Hand
#

game = {
	"holdem" : HoldEmGame,
	"5cardstudhilo" : FiveCardStudHiLoGame,
	"fivecardstudhilo" : FiveCardStudHiLoGame,
	"omaha" : OmahaGame,
	"omahahilo" : OmahaHiLoGame,
	}

######################################################################

usage = "usage: %prog [<options>]"
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

if game.has_key(options.game):
	GameClass = game[options.game]
else:
	print "Unknown game type \"%s\"" % options.game
	print "Known games are:"
	for name in game.keys():
		print "\t%s" % name
	sys.exit(1)

game = GameClass(numHands = options.numHands)
HandClass = GameClass.getHandClass()

hands = Hands()

if options.hands is not None:
	for hand in options.hands:
		cards = Cards.fromString(hand)
		hands.addHand(HandClass(cards))
	game.addHands(hands)

board = Board()
if options.board:
	board.fromString(options.board)
	game.setBoard(board)

if options.verbose:
	callback=showHandCallback

	print "Simulating %d games" % options.numGames
	print "%d Hands: %s" % (game.getNumHands(), hands)
	if game.board:
		print "Board: %s" % game.board
elif options.showProgress:
	callback=showProgressCallback
else:
	callback=None

cmd="game.simulateGames(options.numGames, callback=callback)"

if options.profile:
	import profile
	print "Profiling to file %s" % options.profile
	profile.run(cmd, options.profile)
else:
    eval(cmd)

if options.showProgress:
	print

print game.statsToString()

sys.exit(0)

