#!/usr/bin/env python
######################################################################
#
# Given an Omaha/8 hand, return the point value.
#
# $Id$
#
######################################################################

from optparse import OptionParser
import sys
from pyPoker.Hand import OmahaHand

######################################################################

usage = "usage: %prog [<options>] Card1 Card2 Card3 Card4"
parser = OptionParser(usage)

(options, args) = parser.parse_args()

if len(args) != 4:
    print "Must provide 4 cards. (%d provided)" % len(args)
    sys.exit(1)

######################################################################

hand = OmahaHand.fromStrings(args)
value = hand.pointValue()

if value > 10:
    action = "complete"
if value > 25:
    action = "call"
if value > 40:
    action = "raise"
if value > 50:
    action = "reraise"

print "%s : %d : %s" % (hand, value, action)

sys.exit(0)
