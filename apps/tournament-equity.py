#!/usr/bin/env python
######################################################################
#
# Shown tournament equity of players.
#
# $Id$
#
######################################################################

import optparse
import sys

def calculateEquity(stackArray):
    """Given an array of stack sizes, return an 2-D array giving
    percentages of probably player placement. stackArray should be
    an array giving the stack size for each player."""

    totalChips = sum(stackArray)
    numPlayers = len(stackArray)

    # If the the total number of chips is zero, result is just a 2-D
    # array of 0%. (This serves to terminate recursion.)
    if totalChips == 0:
        chancesArray = [ 0.0 ] * numPlayers
        return [ chancesArray ] * numPlayers

    # Array that will hold each player's array giving their chances of
    # finishing in each position. Note: Don't use "[ [0.0]*numPlayers]
    # *numPlayers" here as that will simply create N references of a
    # single array instead of N copies.
    playerArray = [ ]
    for player in range(numPlayers):
        # Each interior array is the chance the player will take Nth
        # place.
        playerArray.append([ 0.0 ] * numPlayers)

    # Now got through, calculate chance each player will finish first
    # and if so, chances of other players finishing 2nd through
    # Nth. Add those to playerArray.
    for player in range(numPlayers):
        firstPlaceChance = float(stackArray[player])/totalChips
        playerArray[player][0] += firstPlaceChance

        if firstPlaceChance == 0.0:
            # This player has no chance of taking first, so we're done
            # with this possibility.
            continue

        # Given this player finishes first, figure out chances for
        # other players finishing 2nd, 3rd, etc. by calling ourself
        # recursively.
        
        # First make a copy of our array of stack sizes so we don't
        # mess it up.
        stacks = []
        stacks.extend(stackArray)

        # Set the stack size of the player who just finished first to
        # zero to remove them from the calculations.
        stacks[player] = 0

        # And call ourselves recursively to figure out 2nd through Nth
        # place.
        playerSecondPlaceArray = calculateEquity(stacks)

        # Add these results back to our original array, offset by one
        # sice they where calculating second place
        for playerIndex in range(numPlayers):
            for placeIndex in range(numPlayers - 1):
                playerArray[playerIndex][placeIndex + 1 ] += firstPlaceChance * playerSecondPlaceArray[playerIndex][placeIndex]
        
    return playerArray

def parseStacks(option, opt_str, value, parser):
    """optparse callback to handle variable number of stacks."""
    value = []
    while parser.rargs:
        # If we encounter another option, we're done
        if parser.rargs[0][0] == "-":
            break
        value.append(int(parser.rargs.pop(0)))
    setattr(parser.values, "stacks", value)
        

def parsePayout(option, opt_str, value, parser):
    """optparse callback to handle variable number of payouts."""
    value = []
    while parser.rargs:
        # If we encounter another option, we're done
        if parser.rargs[0][0] == "-":
            break
        value.append(int(parser.rargs.pop(0)))
    setattr(parser.values, "payout", value)
        
def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option("-p", "--payout",
                      action="callback", callback=parsePayout)
    parser.add_option("-s", "--stacks",
                      action="callback", callback=parseStacks)
    (options, args) = parser.parse_args(argv)
    print options.stacks
    print options.payout

    #stacks = [8200, 3800, 0, 800]
    #payout = [90, 54, 26]

    playerChances = calculateEquity(options.stacks)
    numPlayers = len(options.stacks)
    for player in range(numPlayers):
        print "%8d: " % options.stacks[player],
        for place in range(numPlayers):
            print " %4.1f%%" % (playerChances[player][place] * 100),
        equity = 0.0
        for place in range(numPlayers):
            if place < len(options.payout):
                equity += playerChances[player][place] * options.payout[place]
        print "  $%.2f" % equity
    return 0

if __name__ == "__main__":
    sys.exit(main())

