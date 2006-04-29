#!/usr/bin/env python
######################################################################
#
# Profile a HoldEmGame
#
# $Id$
#
######################################################################

import profile
import pstats
from pyPoker.PokerGame import HoldEmGame
from pyPoker.Hand import HoldEmHand, Board
import sys

statsFile = "profile/holdem-pstats"

def callback(game):
    if game.gameNum % 10 == 0:
	print ".",
	sys.stdout.flush()

def doit():
    game = HoldEmGame()
    game.setBoard(Board.fromString("5C 2S 4D"))
    game.addHand(HoldEmHand.fromString("AC 2C"))
    game.addHand(HoldEmHand.fromString("AH KH"))
    game.simulateGames(numGames=100, callback=callback)
    print

profile.run('doit()', statsFile)
stats = pstats.Stats(statsFile)
stats.strip_dirs().sort_stats("cumulative").print_stats(20)
