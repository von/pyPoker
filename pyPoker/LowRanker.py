"""Class for ranking poker hands"""

from Cards import Rank
from PokerException import PokerInternalException
from PokerRank import PokerRank
from Ranker import RankerBase

class LowRanker(RankerBase):
    """Given a Hand, return its PokerRank for low.

    Ignores straights and flushes (i.e. wheel is best low hand)."""

    @classmethod
    def rankHand(cls, hand):
        """Given a Hand return a PokerRank for its best hand.

        Limited to Hands of five to seven cards."""
        hand.makeAcesLow()
        # Iterate through all the possible sets of cards in hand and
        # find the highest rank
        lowRank = None
        for cards in hand.hands():
            rank = cls._rankHand(cards)
            if (lowRank is None) or (rank < lowRank):
                lowRank = rank
        return lowRank

    @classmethod
    def bestHand(cls, hands):
        """Riven an array of hands, return the best hands and their rank.

        Returns an array of best hand indexes (even if there is just
        one) and the rank of those hands."""
        best_hands = []
        best_rank = None
        for index, hand in enumerate(hands):
            rank = cls.rankHand(hand)
            if (best_rank is None) or (rank < best_rank):
                best_hands = [index]
                best_rank = rank
            elif best_rank == rank:
                best_hands.append(index)
        return best_hands, best_rank

    @classmethod
    def _rankHand(cls, hand):
        """Given a Hand, return its PokerRank for its best low hand.

        Limited to Hands of 5-7 cards."""
        if len(hand) > 7:
            raise ValueError("Hand has too many cards (%d > 7)" % len(hand))
        if len(hand) < 5:
            raise ValueError("Hand has too few cards (%d < 5)" % len(hand))
        rankCounts = hand.countRanks()
        # Count ranks which we have at least one of
        atLeastOne = filter(lambda rank: rankCounts[rank] > 0, Rank.rankRange)
        # If we don't have at least two different ranks, we have five-of-a-kind
        if len(atLeastOne) < 2:
            raise PokerInternalException("Apparently have five of a kind with hand %s" % hand)
        if len(atLeastOne) >= 5:
            # We can make a hand without a pair
            return PokerRank.highCard(atLeastOne[4], atLeastOne[0:4])

        # We didn't find 5 unpaired cards, figure out where we stand
        atLeastTwo = filter(lambda rank: rankCounts[rank] > 1, Rank.rankRange)
        if len(atLeastTwo) == 0:
            raise PokerInternalException("Invalid state (no pair) with hand %s" % hand)
        if len(atLeastOne) == 4:
            # We will have one pair which will be lowest rank remaining
            pairRank = atLeastTwo[0]
            # Remove pair to obtain kickers
            atLeastOne.remove(pairRank)
            return PokerRank.pair(pairRank, atLeastOne)
        elif (len(atLeastOne) == 3) & (len(atLeastTwo) >= 2):
            # We have two pair
            pairRank1 = atLeastTwo[0]
            pairRank2 = atLeastTwo[1]
            # Remove pairs to obtain kicker
            atLeastOne.remove(pairRank1)
            atLeastOne.remove(pairRank2)
            return PokerRank.twoPair(pairRank1, pairRank2, atLeastOne)

        # If we reach this point, we have at least trips.
        atLeastThree = filter(lambda rank: rankCounts[rank] > 2, Rank.rankRange)
        if len(atLeastThree) == 0:
            raise PokerInternalException("Invalid state (no trips) with hand %s" % hand)
        if len(atLeastOne) == 3:
            tripsRank = atLeastThree[0]
            # Remove trips to obtain kickers
            atLeastOne.remove(tripsRank)
            return PokerRank.trips(tripsRank, atLeastOne)

        # If we reach this point, we have a full house or quads
        if len(atLeastOne) != 2:
            raise PokerInternalException("Invalid state (less than two ranks) with hand %s" % hand)
        if len(atLeastTwo) > 1:
            # Remove trips from pairs to find full house fillers
            tripsRank = atLeastThree[0]
            atLeastTwo.remove(tripsRank)
            return PokerRank.fullHouse(tripsRank, atLeastTwo[0])

        # If we reach this point, we have quads
        atLeastFour = filter(lambda rank: rankCounts[rank] > 3, Rank.rankRange)
        if len(atLeastFour) == 0:
            raise PokerInternalException("Invalid state (no quads) with hand %s" % hand)
        quadsRank = atLeastFour[0]
        # Remove quads to obtain kicker
        atLeastOne.remove(quadsRank)
        return PokerRank.quads(quadsRank, atLeastOne)

