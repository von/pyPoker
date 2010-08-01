#!/usr/bin/env python
"""Unit tests for BitField module."""

from pyPoker.BitField import BitField
import unittest

class TestBitField(unittest.TestCase):

    # Value of a bitfield completely set to ones
    fullMask = 2**32 - 1

    def testCreate(self):
        """Test basic BitField creation."""
        zero = BitField(0)
        one = BitField(1)
        thousand = BitField(1000)
        
    def testMask(self):
        """Test mask() method."""
        m = BitField.mask(numBits=4)
        self.assertEqual(m, 15, "mask value is %s" % m)
        m = BitField.mask(numBits=2, offset=3)
        self.assertEqual(m, 24, "mask value is %s" % m)
        m = BitField.mask(numBits=7, offset=1)
        self.assertEqual(m, 254, "mask value is %s" % m)
        m = BitField.mask(numBits=2, offset=10)
        self.assertEqual(m, 3072, "mask value is %s" % m)

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
 
    def testSetBitRange(self):
        """Test setBitRange() method."""
        value = BitField(128)
        value.setBitRange(numBits=4)
        self.assertEqual(value, 128+15, "Value is %s" % value)
        value = BitField(15)
        value.setBitRange(offset = 3, numBits=5, value=31)
        self.assertEqual(value, 255, "Value is %s" % value)
        value = BitField(0)
        value.setBitRange(offset = 4, numBits=1, value = 255)
        self.assertEqual(value, 16, "Value is %s" % value)
        value = BitField(255)
        value.setBitRange(offset = 0, numBits=8, value = 179)
        self.assertEqual(value, 179, "Value is %s" % value)

    def testGetBitRange(self):
        """Test getBitRange() method."""
        value = BitField(15)
        self.assertEqual(value.getBitRange(numBits=3), 7)
        self.assertEqual(value.getBitRange(numBits=5, offset=3, shift=True), 1)
        self.assertEqual(value.getBitRange(numBits=2, offset=2, shift=True), 3)

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

    def testInvert(self):
        """Test inversion operator."""
        value = ~BitField(15)
        self.assertEqual(value, self.fullMask - 15, "Value is %s" % value)
        value = BitField(255)
        value.invert()
        self.assertEqual(value, self.fullMask - 255, "Value is %s" % value)

if __name__ == "__main__":
    unittest.main()
