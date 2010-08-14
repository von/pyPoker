######################################################################
#
# BitField.py
#
# Classes for representing and manipulating bitfields.
#
# Kudos: http://wiki.python.org/moin/BitManipulation
#
######################################################################

class BitField(int):
    defaultLength = 31

    @staticmethod
    def __new__(cls, value=0, length=None):
        self = super(BitField, cls).__new__(cls, value)
        if not length:
            length = cls.defaultLength
        self.length = length
        return self

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
        # Kudos Brian Kernighan
        # http://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetKernighan
        count = 0
        value = self.toInt()
        while (value):
            value &= value - 1 # This clears lowest bit
            count += 1
        return count

    def lowestSet(self):
        """Returns offset of lowest bit set.

        If value is zero, a ValueError is thrown."""
        if self == 0:
            raise ValueError("Tried to determine lowest bit of zero.")
        # Taking the AND of value and its compliment will leave
        # just the lowest bit set. Kudos:
        # http://wiki.python.org/moin/BitManipulation
        justLow = (self & -self)
        return shiftsUntilZero(justLow) - 1

    def lowestNSet(self, n):
        """Reutrns array of offsets of lowest n bits set.

        Array will be ordered from high to low.
        If value has less than n bits set, returns array of less than length n."""
        if (n == 0) or (self == 0):
            return []
        bits = []
        offset = 0
        value = self
        while ((n > 0) & (value > 0)):
            if value & 0x01:
                bits.insert(0, offset)
                n -= 1
            value >>= 1
            offset += 1
        return bits

    def highestSet(self):
        """Returns offset of highest bit set.

        if value is zero, a ValueError is thrown."""
        if self == 0:
            raise ValueError("Tried to determine highest bit of zero.")
        return shiftsUntilZero(self) - 1

    def highestNSet(self, n):
        """Return array of offsets of highest n bits set.

        Array will be ordered from high to low.
        If value has less than n bits set, returns array of less than length n."""
        if (n == 0) or (self == 0):
            return []
        highestOffset = self.highestSet()
        bits = [highestOffset]
        offset = highestOffset - 1
        while ((len(bits) < n) & (offset >= 0)):
            if self.testBit(offset):
                bits.append(offset)
            offset -= 1
        return bits        

    def testBit(self, offset):
        """Return True if bit at given offset is set."""
        mask = 1 << offset
        return (self & mask != 0)

    def testBits(self, bitfield):
        """Return True if all bits in bitfield are set."""
        return (self & bitfield == bitfield)

    # add(+) and subtract(-) set and clear a bit respectively
    def __add__(self, offset):
        """Set bit at offset."""
        return BitField(super(BitField, self).__or__(1<<offset))

    def __sub__(self, offset):
        """Clear bit at offset."""
        return BitField(super(BitField, self).__and__(~(1<<offset)))

    def filterBits(self, *args):
        """Return BitField with given bits removed."""
        mask = BitField(0)
        for bit in args:
            mask += bit
        return self.__and__(~mask)

    def getBitRange(self, numBits, offset=0, shift=False):
        """Get value contained in numbits at offset.

        If shift is True, then shift bits by offset so they start at 0."""
        mask = (2**numBits - 1) << offset
        value = self & mask
        if shift:
            value >>= offset
        return value

    def toInt(self):
        """Return value of BitField as integer."""
        return int(self)

    def __str__(self):
        """Return binary string presentation.

        Will be multiple of 3 characters."""
        if self == 0:
            return '000'
        s=''
        t={'0':'000','1':'001','2':'010','3':'011',
           '4':'100','5':'101','6':'110','7':'111',
           'L':'' # L is appears at end for longs
           }
        for c in oct(self)[1:]:
            s+=t[c]
        return s

    def __lshift__(self, other):
        """Shift left, hndingling length."""
        mask = super(BitField, self).__lshift__(self.length) - 1
        newValue = super(BitField, self).__lshift__(other) & mask
        return BitField(newValue)

    def __invert__(self):
        newValue = BitField.mask(numBits = self.length)
        newValue ^= self
        return newValue

    # Override functions to return BitField
    def __and__(self, value):
        return BitField(super(BitField, self).__and__(value))

    def __or__(self, value):
        return BitField(super(BitField, self).__or__(value))

    def __xor__(self, value):
        return BitField(super(BitField, self).__xor__(value))

    def __rshift__(self, offset):
        return BitField(super(BitField, self).__rshift__(offset))

######################################################################
#
# Supporting functions
#
def shiftsUntilZero(value):
    """How many times does value have to be shifted right until it is zero?"""
    shifts = 0
    while(value):
        value >>= 1
        shifts += 1
    return shifts
