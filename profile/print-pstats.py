#!/usr/bin/env python
######################################################################
#
# Print pstats from file.
#
# $Id$
#
######################################################################

import pstats
from optparse import OptionParser
import sys

######################################################################

myName = sys.argv[0]
usage = "usage: %prog [<options>] <pstats file>"
parser = OptionParser(usage)
(options, args) = parser.parse_args()

try:
    pstatsFilename = args.pop(0)
except:
    print "%s: pstats file missing." % myName
    sys.exit(1)

######################################################################

stats = pstats.Stats(pstatsFilename)
stats.strip_dirs().sort_stats("cumulative").print_stats(20)
    
