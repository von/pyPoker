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

    Return an iterator returning all the subsets of length n from set."""
    if len(set) < n:
	raise IndexError("Not enough elements (asked for %d, only have %d)" %
			 (n, len(set)))
    elif len(set) == n:
	# Optimization. To keep the same semantics, we make a copy of the
	# passed in set.
	yield set.__class__(set)
    else:
	setLen = len(set)
	# iters will hold an array of n iterators that will progress through
	# the index values of the set
	iters = [rangeIter(setLen - n + 1)]
	# values holds the index values of the current subset
	values = [0] * n
	values[0] = iters[0].next()
	# What iterator is currently progressing
	level = 1
	while True:
	    # Fill array of iterators and corresponding values up
	    while level < n:
		iters.append(rangeIter(values[level - 1] + 1,
				   setLen - n + level + 1))
		values[level]=iters[level].next()
		level += 1
	    yield set.__class__([set[i] for i in values])
	    while True:
		# Get next value at lowest level, if they iterator is done
		# remove it from the iters array and go up a level until
		# we find one that isn't done. while loop above will then
		# fill array back in.
		# If we reach level 0, then topmost iterator has completed
		# and we're done.
		try:
		    values[level - 1] = iters[level - 1].next()
		    break
		except StopIteration:
		    # Last iterator in array is done, remove it and go to
		    # previous iterator.
		    iters.pop()
		    level -= 1
		    if level == 0:
			# Top-level iterator is done, so we are too
			raise StopIteration
		    # Loop back and try again
	
