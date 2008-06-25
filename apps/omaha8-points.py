#!/usr/bin/env python
"""Given an Omaha/8 hand, return the point value."""

from optparse import OptionParser
import sys
from pyPoker.Hand import OmahaHand

######################################################################

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

    usage = "usage: %prog [<options>] <card1> <card2> <card3> <card4>"
    version = "%prog version " + getVersionString()
    parser = OptionParser(usage=usage, version=version)

    (options, args) = parser.parse_args()

    if len(args) != 4:
        print "Must provide 4 cards. (%d provided)" % len(args)
        parser.print_help()
        sys.exit(1)

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

if __name__ == "__main__":
    sys.exit(main())


