"""Internal utility functions"""

import collections
import itertools
import sys

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

class UserSelection(object):
    """Present a user with a menu of options, each selectable with a single
    keystroke. Get and return the user's selection."""

    _Option = collections.namedtuple('_Option', "description return_value")

    def __init__(self,
                 input_stream=None,
                 output_stream=None,
                 prompt="Selection?",
                 selection_format="({})"):
        """input_stream is the stream from which to receive input
        from the user.

        output_stream is the stream to which to send output to the user.

        prompt is the string presented to the user to prompt for
        their selection.

        selection_format is the string used to present the selection
        format to the user. It must include one '{}' string which will
        be replaced by the selection character.
        """
        self.input_stream = input_stream \
            if input_stream is not None else sys.stdin
        self.output_stream = output_stream \
            if output_stream is not None else sys.stdout
        self.prompt = prompt
        self.selection_format = selection_format
        self.options = {}

    def add_option(self, char, description, return_value):
        """Add an option.

        char is the character the user should use to select the option.

        description is the string displayed to the user for the option.

        return_value is the value returned if the user selects the option.
        """
        if char in self.options.keys():
            raise ValueError(\
                "Selection character \"{}\" already in use".format(char))
        self.options[char] = self._Option(description=description,
                                          return_value=return_value)

    def get_user_selection(self):
        """Present user with options and get their selection.

        Returns selection's associated return_value."""
        for char, option in self.options.items():
            self.output_stream.write(\
                self.selection_format.format(char) +
                " {}\n".format(option.description))
        self.output_stream.write(self.prompt)
        self.output_stream.flush()
        while True:
            selection = self.input_stream.read(1)
            if selection in self.options.keys():
                break
            # Just ignore non-legal selections
        self.output_stream.write("\n")
        self.output_stream.flush()
        return self.options[selection].return_value

