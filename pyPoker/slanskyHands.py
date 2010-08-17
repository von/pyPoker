"Define Slansky hand types"""

import HoldEm

SlanskyHand = {}

# Class 1: AA, KK, QQ, JJ, AKs

SlanskyClass1Hands = HoldEm.Hands.fromGroups("AA", "KK", "QQ", "JJ", "AKs")
SlanskyHand['class1'] = SlanskyClass1Hands

# Class 2: TT, AQs, AJs, KQs, AK

SlanskyClass2Hands = HoldEm.Hands.fromGroups("TT", "AQs", "AJs", "KQs", "AK")
SlanskyHand['class2'] = SlanskyClass2Hands


# Class 3: 99, JTs, QJs, KJs, ATs, AQ

SlanskyClass3Hands = HoldEm.Hands.fromGroups("99", "JTs", "QJs",
					    "KJs", "ATs", "AQ")
SlanskyHand['class3'] = SlanskyClass3Hands

# Class 4: T9s, KQ, 88, QTs, 98s, J9s, AJ, KTs

SlanskyClass4Hands = HoldEm.Hands.fromGroups("T9s", "KQ", "88", "QTs", "98s",
					    "J9s", "AJ", "KTs")
SlanskyHand['class4'] = SlanskyClass4Hands

# Class 5: 77, 87s, Q9s, T8s, KJ, QJ, JT, 76s, 97s, Axs, 65s

SlanskyClass5Hands = HoldEm.Hands.fromGroups("77", "87s", "Q9s", "T8s",
					    "KJ", "QJ", "JT", "76s",
					    "97s", "65s")
SlanskyClass5Hands.addSuitedAceXHands()
SlanskyHand['class5'] = SlanskyClass5Hands


# Class 6: 66, AT, 55, 86s, KT, QT, 54s, K9s, J8s, 75s

SlanskyClass6Hands = HoldEm.Hands.fromGroups("66", "AT", "55", "86s", "KT",
					    "QT", "54s", "K9s", "J8s", "75s")
SlanskyHand['class6'] = SlanskyClass6Hands

# Class 7: 44, J9, 64s, T9, 53s, 33, 98, 43s, 22, Kxs, T7s, Q8s

SlanskyClass7Hands = HoldEm.Hands.fromGroups("44", "J9", "64s", "T9", "53s",
					    "33", "98", "43s", "22", "T7s",
					    "Q8s")
# XXX K9s added both here and in class 6
SlanskyClass7Hands.addSuitedKingXHands()
SlanskyHand['class7'] = SlanskyClass7Hands

# Class 8: 87, A9, Q8, 76, 42s, 32s, 96s, 85s, J8, J7s, 65, 54, 74s, K9, T8

SlanskyClass8Hands = HoldEm.Hands.fromGroups("87", "A9", "Q8", "76", "42s",
					    "32s", "96s", "85s", "J8", "J7s",
					    "65", "54", "74s", "K9", "T8")
SlanskyHand['class8'] = SlanskyClass8Hands
