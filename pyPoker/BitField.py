######################################################################
#
# BitField.py
#
# Classes for representing and manipulating bitfields.
#
# Kudos: http://wiki.python.org/moin/BitManipulation
#
######################################################################

class BitField:
    defaultLength = 32

    def __init__(self, value=0, length=None):
        self.value = value
        if not length:
            length = self.defaultLength
        self.length = length

    @classmethod
    def mask(cls, numBits, offset=0, length=None):
        """Create a mask of numBits of 1 at offset."""
        if numBits == 0:
            return BitField(0)
        m = 2 ** numBits - 1
        if not length:
            length = min(cls.defaultLength, offset+numBits)
        return BitField(m << offset, length=length)

    def setCount(self):
        """Return number of bits set."""
        count = 0
        value = self.value
        while (value):
            value &= value - 1 # This clears lowest bit
            count += 1
        return count

    def lowestSet(self):
        """Returns offset of lowest bit set.

        If value is zero, a ValueError is thrown."""
        if self.value == 0:
            raise ValueError("Tried to determine lowest bit of zero.")
        # Taking the AND of value and its compliment will leave
        # just the lowest bit set.
        justLow = (self.value & -self.value)
        return shiftsUntilZero(justLow) - 1

    def highestSet(self):
        """Returns offset of highest bit set.

        if value is zero, a ValueError is thrown."""
        if self.value == 0:
            raise ValueError("Tried to determine lowest bit of zero.")
        return shiftsUntilZero(self.value) - 1

    def testBit(self, offset):
        """Return True if bit at given offset is set."""
        mask = 1 << offset
        return (self.value & mask != 0)

    def setBit(self, offset):
        """Set bit at given offset."""
        self.value |= 1 << offset

    def setBitRange(self, numBits, value=None, offset=0):
        """Set numbits at offset to value if given or all ones otherwise."""
        if value is None:
            value = 2**numBits - 1
        # Shift value to offset and make sure it fits in numBits
        value <<= offset
        mask = (2**numBits - 1) << offset
        value &= mask
        # Clear any existing value in bits and set
        self.value &= ~mask
        self.value |= value
       
    def getBitRange(self, numBits, offset=0, shift=False):
        """Get value contained in numbits at offset.

        If shift is True, then shift bits by offset so they start at 0."""
        mask = (2**numBits - 1) << offset
        value = self.value & mask
        if shift:
            value >>= offset
        return value

    def clearBit(self, offset):
        """Clear bit at given offset."""
        self.value &= ~(1 << offset)

    def clearBits(self, numBits, offset=0):
        """Clear numbBits at offset."""
        if numBits == 0:
            return
        self.value &= ~BitField.mask(numBits=numBits, offset=offset)

    def filter(self, numBits, offset=0):
        """Clear bits outset of numBits at offset."""
        mask = BitField.mask(numBits=numBits, offset=offset)
        mask.invert()
        self &= mask

    def toggleBit(self, offset):
        """Toggle bit at given offset."""
        self.value ^= 1 << offset

    def invert(self):
        """Invert all bits."""
        mask = 2**self.length - 1
        self.value ^= mask

    def __str__(self):
        """Return binary string presentation.

        Will be multiple of 3 characters."""
        if self.value == 0:
            return '000'
        s=''
        t={'0':'000','1':'001','2':'010','3':'011',
           '4':'100','5':'101','6':'110','7':'111',
           'L':'' # L is appears at end for longs
           }
        for c in oct(self.value)[1:]:
            s+=t[c]
        return s

    # Override methods to use self.value
    def __lt__(self, other):
        return self.value < getOtherValue(other)

    def __le__(self, other):
        return self.value <= getOtherValue(other)

    def __eq__(self, other):
        return self.value == getOtherValue(other)

    def __ne__(self, other):
        return self.value != getOtherValue(other)

    def __gt__(self, other):
        return self.value > getOtherValue(other)

    def __ge__(self, other):
        return self.value >= getOtherValue(other)

    def __cmp__(self, other):
        return cmp(self.value, getOtherValue(other))

    def __and__(self, other):
        return BitField(self.value & getOtherValue(other))

    def __xor__(self, other):
        return BitField(self.value ^ getOtherValue(other))

    def __or__(self, other):
        return BitField(self.value | getOtherValue(other))

    def __lshift__(self, other):
        mask = 2**self.length - 1
        newValue = (self.value << other) & mask
        return BitField(newValue)

    def __rshift__(self, other):
        return BitField(self.value >> other)

    def __invert__(self):
        newValue = BitField.mask(numBits = self.length)
        newValue ^= self.value
        return newValue

######################################################################
#
# Supporting functions
#

def getOtherValue(other):
    """Get value of other for overriding methods."""
    if isinstance(other, BitField):
        return other.value
    return other # Assume int or similar

def shiftsUntilZero(value):
    """How many times does value have to be shifted right until it is zero?"""
    shifts = 0
    while(value):
        value >>= 1
        shifts += 1
    return shifts
