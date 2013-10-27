"""Omaha Classes"""

import itertools

from Cards import Rank, Suit
from Hand import CommunityCardHand, FiveCardBoard
from LowRanker import EightLowRanker
import PokerGame
from Utils import assertInstance

class Hand(CommunityCardHand):
    maxCards = 4
    boardClass = FiveCardBoard

    def __init__(self, cards = None, board = None):
	"""Create a Omaha hand.
	cards should be None or an array of up to four cards.
	board should be a Board object."""
	CommunityCardHand.__init__(self, cards, board = board)

    def hands(self):
	"""Return all sets of cards that can be constructed from hand."""
	for hand in self.combinations(5):
	    yield hand

    def combinations(self, n):
	"""Generator function return all combinations of n cards (including
	community cards)."""
	assertInstance(n, int)
	holeCards = self.getHoleCards()
	if n <= 2:
	    for holeCombo in holeCards.combinations(n):
		yield holeCombo
	elif self.board:
	    for holeCombo in holeCards.combinations(2):
		for boardCombo in self.board.combinations(n-2):
		    combo = holeCombo.copy()
		    combo.extend(boardCombo)
		    yield combo
	else:
	    raise NotEnoughCardsException("Cannout generated hand of %d cards without board." % n)

    def combinations_of_eight_or_lower(self, n):
        """Generator function returns all combinations (including community
        cards) of n cards that are 8 or lower (including aces).

        If player doesn't have two hole cards 8 or lower, always
        returns nothing.

        If there aren't n cards 8 or lower, return noths."""
        # Must use two cards from hole cards
        hole_cards = self.getEightOrLower().removeDuplicateRanks()
        if len(hole_cards) < 2:
            return iter([])
        if self.board:
            board_cards = self.board.getEightOrLower().removeDuplicateRanks()
        else:
            board_cards = Cards()
        # If we can't make n cards only using 2 from board, return nothing
        if (len(board_cards) + 2) < n:
            return iter([])
        if n <= 2:
            return hole_cards.combinations(2)
        else:
            return self._combinations(hole_cards, board_cards, n)

    @classmethod
    def _combinations(cls, hole_cards, board_cards, n):
        """Return generator of n cards using 2 hole_cards and board_cards.

        n must be > 2."""
        assert(n>2)
        for hole_combo in hole_cards.combinations(2):
            for board_combo in board_cards.combinations(n-2):
                # Make copy so we don't distubte original
                combo = hole_combo.copy()
                combo.extend(board_combo)
                yield combo

    def eightLowPossible(self):
	"""Return true if this hand can have a eight or better low."""
	return (self.countEightOrLower() >= 2)

    def pointValue(self):
	"""Return the point value of the hand as defined by:
http://casinogambling.about.com/cs/poker/a/omahahilo_2.htm"""
	total = 0
	# Count pairs. A pair adds points equal to rank of card, 30 for aces.
	# Give half-credit for trips and none for quads
	for rank in Rank.ranks:
	    value = rank
	    if rank == Rank.ACE:
		value = 30
	    count = self.rankCount(rank)
	    if count == 2:
		total += value
	    elif count == 3:
		total += value/2
	# Count flushes. Two-flush with Ace gives 10 points, 4 points otherwise.
	# Half credit for three or four flush
	for suit in Suit.suits:
	    suitedCards = self.suitedCards(suit)
	    if suitedCards.rankCount(Rank.ACE) > 0:
		value = 10
	    else:
		value = 4
	    if len(suitedCards) == 2:
		total += value
	    elif len(suitedCards) > 2:
		total += value/2
	# Count straights
	# A two-straight with no or 1-card gap is two points
	for rank in range(Rank.SIX, Rank.ACE + 1):
	    for rank2 in range(rank - 2, rank):
		if self.rankCount(rank) and self.rankCount(rank2):
		    total += 2
	# High Cards. Unpaired Ace is 4 points, unpaired King in 2 points.
	if self.rankCount(Rank.ACE) == 1:
	    total += 4
	if self.rankCount(Rank.KING) == 1:
	    total += 2
	# Count low hands
	# A-2 is 20 points, A-3 is 15, 2-3 and A-4 is 10.
	# Other two babies are 5 points.
        self.makeAcesLow()
	for rank in range(Rank.ACE_LOW, Rank.FIVE):
	    for rank2 in range(rank + 1, Rank.SIX):
		if self.rankCount(rank) and self.rankCount(rank2):
		    if rank == Rank.ACE_LOW:
			if rank2 == Rank.TWO:
			    total += 20
			elif rank2 == Rank.THREE:
			    total += 15
			elif rank2 == Rank.FOUR:
			    total += 10
		    elif rank == Rank.TWO and rank2 == Rank.THREE:
			total += 10
		    else:
			total += 5
        self.makeAcesHigh()
	return total

    def openingHand(self):
	"""Is this an opening hand according to "Winning Omaha 8 Poker" by
Tenner and Krieger?"""
	# A2xx
	if self.rankCount(Rank.ACE):
	    if self.rankCount(Rank.TWO):
		# A3xx
		return True
	    if self.rankCount(Rank.THREE):
		if self.haveSuitedAce():
		    # As3xx	
		    return True
		if self.bigCardCount() == 3:
		    # A3XX
		    return True
	    if self.babyCount() > 2:
		# Abbx
		return True
	    if self.haveSuitedAce() and self.bigCardCount() > 2:
		# AsXXx
		return True
	if self.babyCount() == 4:
	    # bbbb
	    return True
	if self.bigCardCount() == 4:
	    # XXXX
	    return True
	return False

class Simulator(PokerGame.Simulator):
    """Omaha Simulator"""

    HandClass=Hand
    GAME_NAME="Omaha"

    def __init__(self,
                 number_of_hands=9,
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
    """Omaha HiLo (8-or-better) Simulator"""

    LowRankerClass=EightLowRanker
    GAME_NAME="Omaha Hi/Lo 8-or-better"

    def __init__(self,
                 number_of_hands=9,
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


