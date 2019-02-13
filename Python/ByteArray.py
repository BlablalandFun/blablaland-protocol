from collections import deque


def intToByte(val):
    return val.to_bytes(1, 'big')


def byteToInt(val):
    return int.from_bytes(val, 'big')


class ByteArray(object):
    def __init__(self, data=None):
        if data is None:
            data = deque()
        self.bytes = data
        self.position = 0

    def __len__(self):
        return len(self.bytes)

    def __getitem__(self, item):
        return self.bytes[item]

    def __str__(self):
        return self.bytes

    def __del__(self):
        self.reset()

    def read(self, length: int):
        self.position += length
        return self[self.position - length:self.position]

    def writeByte(self, val: int):
        return self.writeBytes(val)

    def readByte(self):
        return int.from_bytes(self.read(1), 'big', signed=True)

    def writeUnsignedByte(self, val: int):
        return self.writeBytes(intToByte(val))

    def readUnsignedByte(self):
        return int.from_bytes(self.read(1), 'big')

    def writeBytes(self, val):
        self.bytes.append(val)
        return self

    def readBytes(self, length: int):
        return self.read(length)

    def writeBoolean(self, val: bool):
        return self.writeByte(1 if val else 0)

    def readBoolean(self):
        return bool(self.readByte())

    def writeUnsignedShort(self, val: int):
        return self.writeBytes(val.to_bytes(2, 'big'))

    def readUnsignedShort(self):
        return int.from_bytes(self.read(2), 'big')

    def writeUnsignedInt(self, val: int):
        return self.writeBytes(val.to_bytes(4, 'big'))

    def readUnsignedInt(self):
        return int.from_bytes(self.read(4), 'big')

    def reset(self):
        self.bytes = deque()
        self.position = 0
