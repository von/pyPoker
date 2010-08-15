#!/usr/bin/env python
"""Unit tests for BitField module."""

from pyPoker.BitField import BitField
import unittest

class TestBitField(unittest.TestCase):

    # Value of a bitfield completely set to ones
    fullMask = BitField.mask(numBits=BitField.defaultLength)

    def testCreate(self):
        """Test basic BitField creation."""
        zero = BitField() # Implicitly 0
        self.assertTrue(isinstance(zero, BitField))
        zero = BitField(0)
        self.assertTrue(isinstance(zero, BitField))
        one = BitField(1)
        thousand = BitField(1000)
        
    def testToInt(self):
        """Test toInt() method."""
        bitfield = BitField(65)
        self.assertTrue(isinstance(bitfield, BitField))
        i = bitfield.toInt()
        self.assertTrue(isinstance(i, int))
        self.assertTrue(i, 65)

    def testMask(self):
        """Test mask() method."""
        m = BitField.mask(numBits=4)
        self.assertTrue(isinstance(m, BitField))
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

    def testLowestNSet(self):
        """Test lowestNSet() method."""
        # assertListEqual() is new in 2.7
        self.assertListEqual(BitField(1).lowestNSet(0), [])
        self.assertListEqual(BitField(1).lowestNSet(1), [0])
        self.assertListEqual(BitField(1).lowestNSet(2), [0])
        self.assertListEqual(BitField(255).lowestNSet(3), [2,1,0])
        self.assertListEqual(BitField(255).lowestNSet(8), [7,6,5,4,3,2,1,0])
        self.assertListEqual(BitField(167).lowestNSet(2), [1,0])
        self.assertListEqual(BitField(167).lowestNSet(4), [5,2,1,0])

    def testHighestSet(self):
        """Test highestSet() method."""
        self.assertRaises(ValueError, BitField(0).highestSet)
        self.assertEquals(BitField(1).highestSet(), 0)
        self.assertEquals(BitField(6).highestSet(), 2)
        self.assertEquals(BitField(96).highestSet(), 6)

    def testHighestNSet(self):
        """Test highestNSet() method."""
        # assertListEqual() is new in 2.7
        self.assertListEqual(BitField(1).highestNSet(0), [])
        self.assertListEqual(BitField(1).highestNSet(1), [0])
        self.assertListEqual(BitField(1).highestNSet(2), [0])
        self.assertListEqual(BitField(255).highestNSet(3), [7,6,5])
        self.assertListEqual(BitField(255).highestNSet(8), [7,6,5,4,3,2,1,0])
        self.assertListEqual(BitField(167).highestNSet(2), [7,5])
        self.assertListEqual(BitField(167).highestNSet(3), [7,5,2])

    def testTestBit(self):
        """Test testBit() method."""
        value = BitField(129)
        self.assertTrue(value.testBit(0), "Value is %s" % value)
        self.assertFalse(value.testBit(1), "Value is %s" % value)
        self.assertTrue(value.testBit(7), "Value is %s" % value)
        self.assertFalse(value.testBit(8), "Value is %s" % value)

    def testTestBits(self):
        """Test testBits() method."""
        value = BitField(15)
        self.assertTrue(value.testBits(7), "Value is %s" % value)
        self.assertFalse(value.testBits(24), "Value is %s" % value)
        self.assertTrue(value.testBits(15), "Value is %s" % value)
        self.assertFalse(value.testBits(31), "Value is %s" % value)

    def testFilterBits(self):
        """Test filterBits() method."""
        value = BitField(255)
        self.assertEqual(value, 255, "Value is %s" % value)
        filtered = value.filterBits() # Should do nothing
        self.assertEqual(filtered, 255)
        filtered = value.filterBits(10) # Should do nothing
        self.assertEqual(filtered, 255)
        filtered = value.filterBits(5)
        self.assertEqual(filtered, 223)
        filtered = value.filterBits(3,2,1,0)
        self.assertEqual(filtered, 240)

    def testAdd(self):
        """Test __add__() method which sets a bit."""
        value = BitField(8)
        self.assertEqual(value, 8, "Value is %s" % value)
        value += 1 # 2
        self.assertEqual(value, 10, "Value is %s" % value)
        self.assertTrue(isinstance(value, BitField), "Type is %s" % type(value))
        value += 7 # 128
        self.assertEqual(value, 138, "Value is %s" % value)
 
    def testGetBitRange(self):
        """Test getBitRange() method."""
        value = BitField(15)
        self.assertEqual(value.getBitRange(numBits=3), 7)
        self.assertEqual(value.getBitRange(numBits=5, offset=3, shift=True), 1)
        self.assertEqual(value.getBitRange(numBits=2, offset=2, shift=True), 3)

    def testSub(self):
        """Test __sub__() method, which clears a bit."""
        value = BitField(65)
        self.assertEqual(value, 65, "Value is %s" % value)
        value -= 0 # 1
        self.assertTrue(isinstance(value, BitField))
        self.assertEqual(value, 64, "Value is %s" % value)
        value -= 0 # 1
        self.assertEqual(value, 64, "Value is %s" % value)
        value -= 1 # 2 
        self.assertEqual(value, 64, "Value is %s" % value)
        value -= 6 # 64
        self.assertEqual(value, 0, "Value is %s" % value)

    def testAND(self):
        """Test AND."""
        value = BitField(76) & 15
        self.assertTrue(isinstance(value, BitField))
        self.assertEqual(value, 12, "Value is %s" % value)

    def testOR(self):
        """Test OR."""
        value = BitField(12) | 72
        self.assertTrue(isinstance(value, BitField))
        self.assertEqual(value, 76, "Value is %s" % value)

    def testXOR(self):
        """Test XOR."""
        value = BitField(76) ^ 15
        self.assertTrue(isinstance(value, BitField))
        self.assertEqual(value, 67, "Value is %s" % value)

    def testLshift(self):
        """Test left shift."""
        value = BitField(67) << 1
        self.assertEqual(value, 134, "Value is %s" % value)

    def testRshift(self):
        """Test right shift."""
        value = BitField(194) >> 1
        self.assertTrue(isinstance(value, BitField))
        self.assertEqual(value, 97, "Value is %s" % value)

    def testInvert(self):
        """Test inversion operator."""
        value = ~BitField(15)
        self.assertTrue(isinstance(value, BitField))
        expectedValue = self.fullMask.toInt() - 15
        self.assertEqual(value, expectedValue, "Value is %s != %s" % (value, expectedValue))
        value = ~BitField(255)
        self.assertTrue(isinstance(value, BitField))
        expectedValue = self.fullMask.toInt() - 255
        self.assertEqual(value, expectedValue, "Value is %s != %s" % (value, expectedValue))

if __name__ == "__main__":
    unittest.main()
