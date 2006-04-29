#!/usr/bin/env python
######################################################################
#
# Set up environment and run test script.
#
######################################################################

import os
import sys

######################################################################

env = os.environ

pypath = os.getcwd()
if env.has_key("PYTHONPATH"):
    pypath += ":" + env["PYTHONPATH"]
env["PYTHONPATH"] = pypath

args = sys.argv
myname = args.pop(0)
try:
    script = args[0]
except:
    print "Usage: %s <script to run>" % myname
    sys.exit(1)
os.execve(script, args, env)
