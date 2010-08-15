#!/usr/bin/env python
"""Unittests for Hands module"""

from pyPoker.Hands import HoldEmHands
from pyPoker.slanskyHands import SlanskyHand
from pyPoker.Cards import Rank
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
	pass

    def testHoldEmHands(self):
	hands = HoldEmHands()
	hands.addHandGroup("AKs")
	self.assertEquals(len(hands), 4)
	hands.__str__()
	hands.addHandGroup("JT")
	self.assertEquals(len(hands), 16)
	hands.__str__()
	hands.addAllHands(Rank.SEVEN, Rank.NINE)
	self.assertEquals(len(hands), 32)
	hands.__str__()
	hands.addPair(Rank.SIX)
	self.assertEquals(len(hands), 38)
	hands.__str__()
	hands.addSuitedAceXHands()
	self.assertEquals(len(hands), 70)
	hands.__str__()
	hands.addSuitedKingXHands()
	self.assertEquals(len(hands), 102)
	hands.__str__()

    def testSlanskyHands(self):
	self.assertEquals(len(SlanskyHand['class1']), 28,
			  "%s - %s" % (len(SlanskyHand['class1']),
				       SlanskyHand['class1']))
	self.assertEquals(len(SlanskyHand['class2']), 30,
			  "%s - %s" % (len(SlanskyHand['class2']),
				       SlanskyHand['class2']))
	self.assertEquals(len(SlanskyHand['class3']), 34,
			  "%s - %s" % (len(SlanskyHand['class3']),
				       SlanskyHand['class3']))
	self.assertEquals(len(SlanskyHand['class4']), 50,
			  "%s - %s" % (len(SlanskyHand['class4']),
				       SlanskyHand['class4']))
	self.assertEquals(len(SlanskyHand['class5']), 98,
			  "%s - %s" % (len(SlanskyHand['class5']),
				       SlanskyHand['class5']))
	self.assertEquals(len(SlanskyHand['class6']), 68,
			  "%s - %s" % (len(SlanskyHand['class6']),
				       SlanskyHand['class6']))
	# When I fix K9s problem, below number will change
	self.assertEquals(len(SlanskyHand['class7']), 106,
			  "%s - %s" % (len(SlanskyHand['class7']),
				       SlanskyHand['class7']))
	self.assertEquals(len(SlanskyHand['class8']), 132,
			  "%s - %s" % (len(SlanskyHand['class8']),
				       SlanskyHand['class8']))

if __name__ == "__main__":
    unittest.main()
