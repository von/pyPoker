######################################################################
#
# Utils.py
#
# Internal utility functions
#
# $Id$
#
######################################################################

def assertInstance(obj, cls):
    if obj is None:
	raise TypeError("Object is None")
    elif isinstance(cls, list):
	for c in cls:
	    if isinstance(obj, c):
		break
	else:
	    raise TypeError("Object not of legal class - %s" % (obj.__class__))
    elif not isinstance(obj, cls):
	raise TypeError("Object not of legal class - %s (%s expected)" % (
		obj.__class__, cls))
