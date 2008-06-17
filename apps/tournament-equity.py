#!/usr/bin/env python
"""Show tournament equity of players.

Given a list of player stack sizes and a payout structure, return each
players equity.

Based on method described in Harrington on Hold'em vol 3, page 2559.
"""

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

def parseIntVarArgs(option, opt_str, value, parser):
    """optparse callback to handle variable number of integers."""
    # Get and append to any existing value
    value = getattr(parser.values, option.dest, [])
    # getattr may return None, in which case we want an empty array
    if value is None:
        value = []
    while parser.rargs:
        arg = parser.rargs[0]
        # If we encounter another option, we're done
        if arg[0] == "-":
            break
        # If not an integer, we done
        try:
            argValue = int(arg)
        except:
            break
        value.append(int(parser.rargs.pop(0)))
    setattr(parser.values, option.dest, value)

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

    usage = "usage: %prog -s <stack1> <stack2>... -p <payout1> <payout2>..."
    version = "%prog version " + getVersionString()
    parser = optparse.OptionParser(usage=usage, version=version)
    parser.add_option("-p", "--payout", dest="payout",
                      action="callback", callback=parseIntVarArgs)
    parser.add_option("-s", "--stacks", dest="stacks",
                      action="callback", callback=parseIntVarArgs)
    (options, args) = parser.parse_args(argv)

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

