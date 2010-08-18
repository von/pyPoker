"""Five Card Stud classes"""

from Hand import StudHand
from PokerGame import PokerGame
from LowRanker import LowRanker 

class Hand(StudHand):
    """A five card stud hand."""
    upCards = [1,2,3,4]
    maxCards = 5


class Game(PokerGame):
    handClass = Hand
    gameName = "Five-card Stud"

class HiLoGame(Game):
    lowHandRankerClass = LowRanker
    gameName = "Five-card Stud Hi/Lo"
