from math import floor

from ByteArray import ByteArray, intToByte
from Constants import GlobalProperties

powList = [2 ** i for i in range(33)]


class Binary(ByteArray):
    def __init__(self, *args):
        super().__init__()
        self.bitLength = 0
        self.bitPosition = 0
        length = len(args)
        if length == 1:
            self.readMessage(list(*args))
        elif length == 2:
            self.writeIdentity(*args)

    def writeIdentity(self, _Id, _subId):
        write = self.bitWriteUnsignedInt
        write(GlobalProperties.BIT_TYPE, _Id)
        write(GlobalProperties.BIT_STYPE, _subId)

    def readIdentity(self):
        read = self.bitReadUnsignedInt
        _type = read(GlobalProperties.BIT_TYPE)
        _stype = read(GlobalProperties.BIT_STYPE)
        return _type, _stype

    def readMessage(self, data: list):
        for (index, char) in enumerate(data):
            if char == 1:
                self.writeByte(1 if data[index + 1] == 2 else 0)
                del data[index + 1]
            else:
                self.writeByte(char)
        self.bitLength = len(self.bytes) * 8
        return self

    def exportMessage(self):
        byte = ByteArray()
        for c in list(self.bytes):
            if c in range(2):
                byte.writeByte(1)
                byte.writeByte(3 if c == 0 else 2)
            else:
                byte.writeByte(c)
        return byte

    def bitReadUnsignedInt(self, param1: int):
        if self.bitPosition + param1 > self.bitLength:
            self.bitPosition = self.bitLength
            return 0
        loc2 = 0
        loc3 = param1
        while loc3 > 0:
            loc4 = int(floor(self.bitPosition / 8))
            loc5 = self.bitPosition % 8
            loc6 = 8 - loc5
            loc7 = min(loc6, loc3)
            loc8 = self[loc4] >> loc6 - loc7 & powList[loc7] - 1
            loc2 += loc8 * powList[loc3 - loc7]
            loc3 -= loc7
            self.bitPosition += loc7
        return loc2

    def bitWriteUnsignedInt(self, param1: int, param2):
        param2 = min(powList[param1] - 1, param2)
        loc3 = param1
        while loc3 > 0:
            loc4 = self.bitLength % 8
            if loc4 == 0:
                self.writeBoolean(False)
            loc5 = 8 - loc4
            loc6 = min(loc5, loc3)
            loc7 = self.rshift(param2, loc3 - loc6)
            self.bytes[-1] += loc7 * powList[loc5 - loc6]
            param2 -= loc7 * powList[loc3 - loc6]
            loc3 -= loc6
            self.bitLength += loc6
        return self

    def bitReadString(self):
        loc1 = ""

        loc2 = self.bitReadUnsignedInt(16)
        for _ in range(loc2):
            loc4 = self.bitReadUnsignedInt(8)
            if loc4 == 255:
                loc4 = 8364
            loc1 += chr(loc4)
        return loc1

    def bitWriteString(self, param1: str):
        loc2 = min(len(param1), powList[16] - 1)
        self.bitWriteUnsignedInt(16, loc2)
        for a in range(loc2):
            loc4 = ord(param1[a])
            if loc4 == 8364:
                loc4 = 255
            self.bitWriteUnsignedInt(8, loc4)
        return self

    def bitReadSignedInt(self, param1: int):
        return self.bitReadUnsignedInt(param1 - 1) * (1 if self.bitReadBoolean() else -1)

    def bitWriteSignedInt(self, param1: int, param2):
        self.bitWriteBoolean(param2 >= 0)
        self.bitWriteUnsignedInt(param1 - 1, abs(param2))
        return self

    def bitReadBinary(self, val: int):
        loc2 = Binary()
        loc3 = self.bitPosition
        while self.bitPosition - loc3 < val:
            if self.bitPosition == self.bitLength:
                return loc2
            loc5 = min(8, val - self.bitPosition + loc3)
            loc2.bitWriteUnsignedInt(loc5, self.bitReadUnsignedInt(loc5))
        return loc2

    def bitWriteBinary(self, binary):
        binary.bitPosition = 0
        loc2 = binary.bitLength
        while loc2:
            loc3 = min(8, loc2)
            self.bitWriteUnsignedInt(loc3, binary.bitReadUnsignedInt(loc3))
            loc2 -= loc3
        return self

    def bitReadBinaryData(self):
        return self.bitReadBinary(self.bitReadUnsignedInt(16))

    def bitWriteBinaryData(self, binary):
        self.bitWriteUnsignedInt(16, int(min(binary.bitLength, powList[16] - 1)))
        self.bitWriteBinary(binary)
        return self

    def bitReadBoolean(self):
        if self.bitPosition == self.bitLength:
            return False
        loc1 = int(floor(self.bitPosition / 8))
        loc2 = self.bitPosition % 8
        self.bitPosition += 1
        return intToByte(self[loc1] >> 7 - loc2 & 1) == intToByte(1)

    def bitWriteBoolean(self, value: bool):
        loc2 = self.bitLength % 8
        if loc2 == 0:
            self.writeBoolean(False)
        if value:
            self.bytes[-1] += powList[7 - loc2]
        self.bitLength += 1
        return self

    @staticmethod
    def rshift(param1, param2):
        return int(floor(param1 / powList[param2]))
