"""Omaha Classes"""

from Cards import Rank, Suit
from Hand import CommunityCardHand, FiveCardBoard
from LowRanker import LowRanker
from PokerGame import CommunityCardPokerGame
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

class Game(CommunityCardPokerGame):
    handClass = Hand
    gameName = "Omaha"

class HiLoGame(Game):
    lowHandRankerClass = LowRanker
    lowHandEightOrBetter = True
    gameName = "Omaha Hi/Lo 8-or-better"
