#!/usr/bin/env python
"""Unit tests for BitField module."""

from pyPoker.BitField import BitField
import unittest

class TestBitField(unittest.TestCase):

    def testCreate(self):
        """Test basic BitField creation."""
        zero = BitField(0)
        one = BitField(1)
        thousand = BitField(1000)
        
    def testComparsion(self):
        """Test BitField comparison methods."""
        self.assertEqual(BitField(0), 0)
        self.assertEqual(BitField(10), 10)
        self.assertTrue(BitField(10) > 7)
        self.assertFalse(BitField(250) > 300)

    def testSetCount(self):
        """Test setCount() method."""
        self.assertEquals(BitField(0).setCount(), 0)
        self.assertEquals(BitField(1).setCount(), 1)
        self.assertEquals(BitField(2).setCount(), 1)
        self.assertEquals(BitField(3).setCount(), 2)
        self.assertEquals(BitField(9).setCount(), 2)
        self.assertEquals(BitField(255).setCount(), 8)
        self.assertEquals(BitField(256).setCount(), 1)

    def testLowestSet(self):
        """Test lowestSet() method."""
        self.assertRaises(ValueError, BitField(0).lowestSet)
        self.assertEquals(BitField(1).lowestSet(), 0)
        self.assertEquals(BitField(6).lowestSet(), 1)
        self.assertEquals(BitField(96).lowestSet(), 5)

    def testHighestSet(self):
        """Test highestSet() method."""
        self.assertRaises(ValueError, BitField(0).highestSet)
        self.assertEquals(BitField(1).highestSet(), 0)
        self.assertEquals(BitField(6).highestSet(), 2)
        self.assertEquals(BitField(96).highestSet(), 6)

    def testTestBit(self):
        """Test testBit() method."""
        value = BitField(129)
        self.assertTrue(value.testBit(0), "Value is %s" % value)
        self.assertFalse(value.testBit(1), "Value is %s" % value)
        self.assertTrue(value.testBit(7), "Value is %s" % value)
        self.assertFalse(value.testBit(8), "Value is %s" % value)

    def testSetBit(self):
        """Test setBit() method."""
        value = BitField(8)
        self.assertEqual(value, 8, "Value is %s" % value)
        value.setBit(1)
        self.assertEqual(value, 10, "Value is %s" % value)
        value.setBit(7)
        self.assertEqual(value, 138, "Value is %s" % value)
 
    def testClearBit(self):
        """Test clearBit() method."""
        value = BitField(65)
        self.assertEqual(value, 65, "Value is %s" % value)
        value.clearBit(0)
        self.assertEqual(value, 64, "Value is %s" % value)
        value.clearBit(0)
        self.assertEqual(value, 64, "Value is %s" % value)
        value.clearBit(1)
        self.assertEqual(value, 64, "Value is %s" % value)
        value.clearBit(6)
        self.assertEqual(value, 0, "Value is %s" % value)

    def testToggleBit(self):
        """Test toggleBit() method."""
        value = BitField(79)
        self.assertEqual(value, 79, "Value is %s" % value)
        value.toggleBit(4)
        self.assertEqual(value, 95, "Value is %s" % value)
        value.toggleBit(4)
        self.assertEqual(value, 79, "Value is %s" % value)

    def testAND(self):
        """Test AND."""
        value = BitField(76) & 15
        self.assertEqual(value, 12, "Value is %s" % value)

    def testOR(self):
        """Test OR."""
        value = BitField(12) | BitField(72)
        self.assertEqual(value, 76, "Value is %s" % value)

    def testXOR(self):
        """Test XOR."""
        value = BitField(76) ^ 15
        self.assertEqual(value, 67, "Value is %s" % value)

    def testLshift(self):
        """Test left shift."""
        value = BitField(67) << 1
        self.assertEqual(value, 134, "Value is %s" % value)

    def testRshift(self):
        """Test right shift."""
        value = BitField(194) >> 1
        self.assertEqual(value, 97, "Value is %s" % value)
        
if __name__ == "__main__":
    unittest.main()
