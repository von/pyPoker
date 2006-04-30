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

######################################################################
#
# Callback for displaying each hand
#

def showHandCallback(game):
	print game.lastGameToString()

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
parser.add_option("-g", "--game", type="string", dest="game",
		  default="holdem", help="game to simulate")
parser.add_option("-n", "--numGames", type="int", dest="numGames",
		  default=100, help="number of games to simulate")
parser.add_option("-N", "--numHands", type="int", dest="numHands",
		  default=10, help="number of hands in play")
parser.add_option("-H", "--hand", type="string", dest="hands",
		  metavar="cards", action="append", help="add a hand")
parser.add_option("-B", "--board", type="string", dest="board",
		  metavar="cards", help="specify the flop")
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
		cards = Cards()
		cards.fromString(hand)
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
else:
	callback=None

game.simulateGames(options.numGames, callback=callback)

highWins = game.getHighWins()
lowWins = game.getLowWins()
scoops = game.getScoops()

for hand in range(game.getNumHands()):
	if hand >= len(hands):
		print "XX " * HandClass.getMaxCards(),
	else:
		print str(hands[hand]) + " ",
	if highWins:
		wins = highWins[hand]
		print "High wins %4d (%6.2f%%)" % (
			wins,
			100.0 * wins / options.numGames),
	if lowWins:
		wins = lowWins[hand]
		print " Low wins %4d (%6.2f%%)" % (
			wins,
			100.0 * wins / options.numGames),
	if scoops:
		scoopWins = scoops[hand]
		print " Scoops: %d" % scoopWins
	else:
		print

sys.exit(0)

