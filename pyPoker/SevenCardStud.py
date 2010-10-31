"""Seven Card Stud classes"""

from Hand import StudHand
from LowRanker import LowRanker
import PokerGame

class Hand(StudHand):
    """A five card stud hand."""
    upCards = [2,3,4,5]
    maxCards = 7

class Simulator(PokerGame.Simulator):
    """Seven-card Stud"""

    HandClass=Hand
    GAME_NAME="Seven-card Stud"

    def __init__(self,
                 number_of_hands=7,
                 predefined_hands=None,
                 predefined_board=None):
        """Initialize simulation.

        number_of_hands is number of hands total to simulate.

        predefined_hands should be a Hands instances and can containe
        either Hand or HandGenerator instances. For a latter a new
        hand will be generated for each simulation.

        predefined_board should be a predefined set of community cards.
        Setting this for a HandClass that doesn't support a board will
        raise an error."""
        PokerGame.Simulator.__init__(self,
                                     number_of_hands=number_of_hands,
                                     predefined_hands=predefined_hands,
                                     predefined_board=predefined_board)

class HiLoSimulator(PokerGame.Simulator):
    """Seven-card Stud HiLo Simulator"""

    LowRankerClass=LowRanker
    GAME_NAME="Seven-card Stud Hi/Lo"

    def __init__(self,
                 number_of_hands=7,
                 predefined_hands=None,
                 predefined_board=None):
        """Initialize simulation.

        number_of_hands is number of hands total to simulate.

        predefined_hands should be a Hands instances and can containe
        either Hand or HandGenerator instances. For a latter a new
        hand will be generated for each simulation.

        predefined_board should be a predefined set of community cards.
        Setting this for a HandClass that doesn't support a board will
        raise an error."""
        PokerGame.Simulator.__init__(self,
                                     number_of_hands=number_of_hands,
                                     predefined_hands=predefined_hands,
                                     predefined_board=predefined_board)

