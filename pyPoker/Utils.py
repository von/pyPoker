"""Internal utility functions"""

import itertools

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


def rangeIter(value1, value2=None):
    """Arguments: [start=0,] stop

    Return an iterator returning start..stop."""
    if value2:
	for value in xrange(value1, value2):
	    yield value
    else:
	for value in xrange(value1):
	    yield value

def rindex(array, value):
    for index in range(len(array)-1,-1,-1):
	if array[index] == value:
	    return index
    raise IndexError

def combinations(set, n):
    """Arguments: set, n

    Return an iterator returning all the subsets of length n from set.
    Note that unlike itertools.combinations() the returned subsets will be
    the same class as set."""
    if len(set) < n:
	raise IndexError("Not enough elements (asked for %d, only have %d)" %
			 (n, len(set)))
    elif len(set) == n:
	# Optimization. To keep the same semantics, we make a copy of the
	# passed in set.
	yield set.__class__(set)
    else:
        for comb in itertools.combinations(set, n):
            yield set.__class__(comb)
	
