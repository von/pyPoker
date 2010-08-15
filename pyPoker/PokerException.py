"""Base class for all pyPoker exceptions."""

class PokerException(Exception):
    """Base class for all poker exceptions in this module."""
    
    def __init__(self, message=None):
	self.value = message

    def __str__(self):
	return self.value

class PokerInternalException(PokerException):
    """Some sort of internal error."""
    pass
