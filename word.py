from byte import Byte

# A Word is four Bytes
class Word:
    def __init__(self, bytes = [0, 0, 0, 0]):
        if (isinstance(bytes[0], Byte)):
            self.bytes = bytes
        else:
            self.bytes = [Byte(x) for x in bytes]

    @classmethod
    def from_4bytes(self, value = 0):
        b0 =  value             >> 24
        b1 = (value & 0xff0000) >> 16 
        b2 = (value &   0xff00) >> 8
        b3 = (value &     0xff)
        return Word([b0, b1, b2, b3])
    
    def __str__(self):
        return str([str(x) for x in self.bytes])
    def __repr__(self):
        return str([str(x) for x in self.bytes])

    def __eq__(self, other):
        return self.bytes == other.bytes

    # `self[key]` operator
    def __getitem__(self, key):
        return self.bytes[key]

    # `self[key] = value` operator 
    def __setitem__(self, key, value):
        self.bytes[key] = value
        return value

    def __xor__(self, other):
        return Word([self.bytes[i] ^ other.bytes[i] for i in range(4)])