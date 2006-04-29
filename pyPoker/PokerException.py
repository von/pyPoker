######################################################################
#
# PokerException.py
#
# Base class for all pyPoker exceptions.
#
# $Id$
#
######################################################################


class PokerException(Exception):
    """Base class for all poker exceptions in this module."""
    
    def __init__(self, message=None):
	self.value = message

    def __str__(self):
	return self.value
