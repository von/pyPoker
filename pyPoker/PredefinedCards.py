######################################################################
#
# PredefinedCards.py
#
# Predefined instances of all the cards.
#
# von@vwelch.com
#
# $Id$
#
######################################################################
"""Provide predefined instances for Cards, Suits and Ranks.

Included instances:

The suits: Spades, Hearts, Diamonds, Clubs
The ranks: Ace, Two, Three, Four, Five, Six, Seven, Eight, Nine
      Ten, Jack, Queen, King
The cards, AceOfClubs, TwoOfClubs, etc.

"""

######################################################################

from Cards import Suit, Rank, Card

######################################################################

for _suit in Suit.suits:
    _name = Suit.suitsLongString[_suit].capitalize()
    exec("%s = Suit(%d)" % (_name, _suit))

for _rank in Rank.ranks:
    _name = Rank.ranksLongString[_rank].capitalize()
    exec("%s = Rank(%d)" % (_name, _rank))

for _suit in Suit.suits:
    for _rank in Rank.ranks:
	_name = "%sOf%s" % (Rank.ranksLongString[_rank].capitalize(),
			    Suit.suitsLongString[_suit].capitalize())
	exec("%s = Card((Rank(%d), Suit(%d)))" % (_name, _rank, _suit))
