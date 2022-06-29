class Byte:
    def __init__(self, value = 0):
        self.value = value

    def __str__(self):
        return hex(self.value)
    def __repr__(self):
        return hex(self.value)

    # `self[key]` operator
    def __getitem__(self, key):
        return int(((self.value >> key & 1) != 0))

    # `self[key] = value` operator 
    def __setitem__(self, key, value):
        if (value != 0): # set bit (i.e. to 1)
            self.value = self.value | (1 << key)
        else:            # clear bit (i.e. to 0)
            self.value = self.value & ~(1 << key)
        return self.value

    # n: 0-1, with 0 = high nibble, 1 = low nibble
    def get_nibble(self, n):
        return (self.value >> 4 & 0xf, self.value & 0xf)[n]

    def __eq__(self, other):
        return self.value == other.value

    def __add__(self, other):
        return Byte(self.value ^ other.value)
    def __xor__(self, other):
        return Byte(self.value ^ other.value)

    def __or__(self, other):
        return Byte(self.value | other.value)
    def __and__(self, other):
        return Byte(self.value & other.value)

    def __lshift__(self, other):
        return Byte(self.value << other)

    # Perform `xtime()` `power_of_x` number of times
    def xtime(self, power_of_x=1):
        result = Byte(self.value)
        for i in range(power_of_x):
            result <<= 1
            if (result[8] != 0):
                result += Byte(0x1b)
                result[8] = 0
        return result

    # Get all bits that are set (i.e. digit's value is 1)
    def set_bits(self):
        return [i for i in range(8) if self[i] != 0]

    # Finite-Field multiply `self` by `other`
    def __mul__(self, other):
        result = Byte(0)
        for bit_digit in other.set_bits():
            result += self.xtime(bit_digit)
        return result