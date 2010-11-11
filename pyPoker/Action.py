"""Classes for representing betting actions"""

from PokerException import PokerException

######################################################################
#
# Exceptions
#

class InvalidActionException(PokerException):
    """Action is invalid."""
    pass

######################################################################

class Action(object):
    """An action by a player (fold, check, call, bet, raise, ante, blind)"""

    TYPE_FOLD = 0x00
    TYPE_CHECK = 0x01
    TYPE_CALL = 0x02
    TYPE_BET = 0x03
    TYPE_RAISE = 0x04
    TYPE_BLIND = 0x05
    TYPE_ANTE = 0x06

    __strs = {
        TYPE_FOLD : "fold",
        TYPE_CHECK : "check",
        TYPE_CALL : "call",
        TYPE_BET : "bet",
        TYPE_RAISE : "raise",
        TYPE_BLIND : "blind",
        TYPE_ANTE : "ante",
        }

    def __init__(self, type, amount=0, all_in=False):
        """Create a Action.

        type must be one of the TYPE_* constants.

        amount must be the amount of the action. For a raise, it must be the
        total bet.

        all_in must be True if this represents an all-in.
        """
        # Todo: Sanity check arguments
        self.type = type
        self.amount = amount
        self.all_in = all_in

    #
    # Creation methods
    #

    @classmethod
    def new_ante(cls, amount, all_in=False):
        """Create a new ante action"""
        return Action(cls.TYPE_ANTE, amount=amount, all_in=all_in)

    @classmethod
    def new_bet(cls, amount, all_in=False):
        """Create a new bet action"""
        return Action(cls.TYPE_BET, amount=amount, all_in=all_in)

    @classmethod
    def new_blind(cls, amount, all_in=False):
        """Create a new blind action"""
        return Action(cls.TYPE_BLIND, amount=amount, all_in=all_in)

    @classmethod
    def new_call(cls, amount, all_in=False):
        """Create a new call action"""
        return Action(cls.TYPE_CALL, amount=amount, all_in=all_in)

    @classmethod
    def new_check(cls):
        """Create a new check action"""
        return Action(cls.TYPE_CHECK)

    @classmethod
    def new_fold(cls):
        """Create a new fold action"""
        return Action(cls.TYPE_FOLD)

    @classmethod
    def new_raise(cls, amount, all_in=False):
        """Create a new raise action"""
        return Action(cls.TYPE_RAISE, amount=amount, all_in=all_in)

    def is_all_in(self):
        """Does this action represent an all-in?"""
        return self.all_in

    #
    # Testing methods
    #

    def is_ante(self):
        """Is this action an ante?"""
        return self.type == self.TYPE_ANTE

    def is_bet(self):
        """Is this action a bet?"""
        return self.type == self.TYPE_BET

    def is_blind(self):
        """Is this action a blind?"""
        return self.type == self.TYPE_BLIND

    def is_call(self):
        """Is this action a call?"""
        return self.type == self.TYPE_CALL

    def is_check(self):
        """Is this action a check?"""
        return self.type == self.TYPE_CHECK

    def is_fold(self):
        """Is this action a fold?"""
        return self.type == self.TYPE_FOLD

    def is_raise(self):
        """Is this action a raise?"""
        return self.type == self.TYPE_RAISE

    def __str__(self):
        s = self.__strs[self.type]
        if self.amount:
            s += " %d" % self.amount
        if self.all_in:
            s += " (all-in)"
        return s

######################################################################

class ActionRequest(object):

    ANTE_REQUEST = 0x00  # Request for a ante
    BLIND_REQUEST = 0x01  # Request for a blind
    OPENING_BET_REQUEST = 0x02   # Bet or check
    CALL_REQUEST = 0x03  # Fold, call or raise
    OPTION_REQUEST = 0x05  # Option to big blind: Check or Raise

    __strs = {
        ANTE_REQUEST : "ante",
        BLIND_REQUEST : "blind",
        OPENING_BET_REQUEST : "opening bet",
        CALL_REQUEST : "call",
        OPTION_REQUEST : "option",
        }

    def __init__(self, type, amount, raise_amount=None):
        self.type = type
        self.amount = amount
        self.raise_amount = raise_amount

    ########################################
    # Creation methods

    @classmethod
    def new_ante_request(cls, amount):
        """Create a request for an ante of the given amount"""
        return ActionRequest(type=cls.ANTE_REQUEST,
                             amount=amount)

    @classmethod
    def new_blind_request(cls, amount):
        """Create a request for a blind of the given amount"""
        return ActionRequest(type=cls.BLIND_REQUEST,
                             amount=amount)

    @classmethod
    def new_opening_bet_request(cls, amount):
        """Create a new opening bet request"""
        return ActionRequest(type = cls.OPENING_BET_REQUEST,
                             amount = amount)

    @classmethod
    def new_call_request(cls, amount, raise_amount=None):
        """Create a new call request"""
        return ActionRequest(type = cls.CALL_REQUEST,
                             amount = amount,
                             raise_amount = raise_amount)

    @classmethod
    def new_option_request(cls, raise_amount):
        """Create a new option request"""
        return ActionRequest(type = cls.OPTION_REQUEST,
                             amount = None,
                             raise_amount = raise_amount)

    ########################################
    # Action validation methods

    def validate_action(self, action):
        """Is this given action a value response to this request?

        Raises an InValidActionException if not."""
        if self.is_ante_request():
            self._check_ante_action(action)
        elif self.is_blind_request():
            self._check_blind_action(action)
        elif self.is_opening_bet_request():
            self._check_opening_bet_action(action)
        elif self.is_call_request():
            self._check_call_action(action)
        elif self.is_option_request():
            self._check_option_action(action)
        else:
            raise InvalidActionException(\
                "Unrecognized request type ({})".format(str(self)))

    def _check_ante_action(self, action):
        """Check action in response to ante request"""
        if action.is_ante():
            self._check_ante(action)
        elif action.is_fold():
            self._check_fold(action)
        else:
            raise InvalidActionException(\
                "Action ({}) is not ante or fold".format(str(action)))

    def _check_blind_action(self, action):
        """Check action in response to blind request"""
        if action.is_blind():
            self._check_blind(action)
        elif action.is_fold():
            self._check_fold(action)
        else:
            raise InvalidActionException(\
                "Action ({}) is not blind or fold".format(str(action)))

    def _check_opening_bet_action(self, action):
        """Check action in response to opening bet request"""
        if action.is_check():
            self._check_check(action)
        elif action.is_bet():
            self._check_bet(action)
        elif action.is_fold():
            self._check_fold(action)
        else:
            raise InvalidActionException(\
                "Action ({}) is not bet, check or fold".format(str(action)))

    def _check_call_action(self, action):
        """Check action in response to call request"""
        if action.is_call():
            self._check_call(action)
        elif action.is_raise():
            self._check_raise(action)
        elif action.is_fold():
            self._check_fold(action)
        else:
            raise InvalidActionException(\
                "Action ({}) is not call, fold or raise".format(str(action)))

    def _check_option_action(self, action):
        """Check action in request to option request"""
        if action.is_check():
            self._check_check(action)
        elif action.is_raise():
            self._check_raise(action)
        else:
            raise InvalidActionException(\
                "Action ({}) is not check or raise".format(str(action)))

    def _check_action_amount(self, action):
        """Validate action amount.

        Raises an InvalidActionException if amount invalid."""
        if (action.amount < self.amount) and not action.is_all_in():
            raise InvalidActionException(\
                "{} amount ({}) less than required ({})".format(\
                    str(self), action.amount, self.amount))
        if action.amount > self.amount:
            raise InvalidActionException(\
                "{} amount ({}) greater than allowed ({})".format(\
                    str(self), action.amount, self.amount)) 

    def _check_ante(self, action):
        """Validate ante action.

        Raises an InvalidActionException if amount invalid."""
        self._check_action_amount(action)

    def _check_blind(self, action):
        """Validate blind action.

        Raises an InvalidActionException if amount invalid."""
        self._check_action_amount(action)

    def _check_call(self, action):
        """Validate call action.

        Raises an InvalidActionException if amount invalid."""
        self._check_action_amount(action)

    def _check_bet(self, action):
        """Validate call action.

        Raises an InvalidActionException if amount invalid."""
        self._check_action_amount(action)

    def _check_raise(self, action):
        """Validate call action.

        Raises an InvalidActionException if amount invalid."""
        if self.raise_amount is None:
            raise InvalidActionException("Raise not allowed")
        elif (action.amount < self.raise_amount) and \
                not action.is_all_in():
            raise InvalidActionException(\
                "Raise amount ({}) less than required ({})".format(\
                    action.amount, self.raise_amount))
        elif action.amount > self.raise_amount:
            raise InvalidActionException(\
                "Raise amount ({}) greater than allowed ({})".format(\
                    action.amount, self.raise_amount))

    def _check_check(self, action):
        """Validate check action"""
        if action.amount != 0:
            raise InvalidActionException(\
                "Check amount ({}) is not zero".format(action.amount))

    def _check_fold(self, action):
        """Validate fold action"""
        if action.amount != 0:
            raise InvalidActionException(\
                "Fold amount ({}) is not zero".format(action.amount))

    ########################################
    # Type test methods

    def is_ante_request(self):
        """Is this a request for an ante?"""
        return self.type == self.ANTE_REQUEST

    def is_blind_request(self):
        """Is this a request of a blind?"""
        return self.type == self.BLIND_REQUEST

    def is_opening_bet_request(self):
        """Is this a request for a opening bet?"""
        return self.type == self.OPENING_BET_REQUEST

    def is_call_request(self):
        """Is this a request for a call?"""
        return self.type == self.CALL_REQUEST

    def is_option_request(self):
        """Is this a request for a option?"""
        return self.type == self.OPTION_REQUEST

    ########################################
    # Other methods

    def __str__(self):
        s = "{} request".format(self.__strs[self.type])
        if self.amount is not None:
            s += " for {}".format(self.amount)
        if self.raise_amount is not None:
            s += " or raise of {}".format(self.raise_amount)
        return s


