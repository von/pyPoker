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

def main(argv=None):
    # Do argv default this way, as doing it in the functional
    # declaration sets it at compile time.
    if argv is None:
        argv = sys.argv
    parser = OptionParser(
        usage="%prog [<options>] <pstats file>", # printed with -h/--help
        version="%prog 1.0" # automatically generates --version
        )
    parser.add_option("-t", "--totalTime",
                      action="store_true", dest="totalTime",
                      help="Just display total time", default=False)
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.error("No pstats filename provided.")
    for filename in args:
        try:
            stats = pstats.Stats(filename)
        except Exception, e:
            print "Error parsing stats file \"%s\": %s" % (filename, e)
            next
        if options.totalTime:
            # I don't know if this argument is supposed to be public or not
            # but it's the only way I can find to get at this information.
            print "%8.3f CPU-sec" % stats.total_tt
        else:
            # Print long stats
            stats.strip_dirs().sort_stats("cumulative").print_stats(20)
    return(0)

if __name__ == "__main__":
    sys.exit(main())

    
