"""Seven Card Stud classes"""

from Hand import StudHand
from PokerGame import PokerGame
from LowRanker import LowRanker

class Hand(StudHand):
    """A five card stud hand."""
    upCards = [2,3,4,5]
    maxCards = 7

class Game(PokerGame):
    handClass = Hand
    gameName = "Seven-card Stud"

class HiLoGame(Game):
    lowHandRankerClass = LowRanker
    gameName = "Seven-card Stud Hi/Lo"
