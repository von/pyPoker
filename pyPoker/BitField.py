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
    def __init__(self, value=0):
        self.value = value

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

    def clearBit(self, offset):
        """Clear bit at given offset."""
        self.value &= ~(1 << offset)

    def toggleBit(self, offset):
        """Toggle bit at given offset."""
        self.value ^= 1 << offset

    def __str__(self):
        """Return binary string presentation.

        Will be multiple of 3 characters."""
        if self.value == 0:
            return '000'
        s=''
        t={'0':'000','1':'001','2':'010','3':'011',
           '4':'100','5':'101','6':'110','7':'111'}
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
        return self.value & getOtherValue(other)

    def __xor__(self, other):
        return self.value ^ getOtherValue(other)

    def __or__(self, other):
        return self.value | getOtherValue(other)

    def __lshift__(self, other):
        return self.value << other

    def __rshift__(self, other):
        return self.value >> other

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
