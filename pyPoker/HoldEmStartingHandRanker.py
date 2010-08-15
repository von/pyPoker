"""Class for ranking starting HoldEm hands"""

from Hand import HoldEmHand
from PokerRank import PokerRank
from Ranker import RankerBase

class HoldEmStartingHandRanker(RankerBase):
    """Rank starting HoldEm hands"""
    
    @classmethod
    def rankHand(cls, hand):
        """Rank a hold'em hand (pair or high card)."""
        if hand[0].rank == hand[1].rank:
            return PokerRank.pair(hand[0].rank, kickers=None)
        if hand[0].rank > hand[1].rank:
            return PokerRank.highCard(hand[0].rank, hand[1:])
        else:
            return PokerRank.highCard(hand[1].rank, hand[:1])
