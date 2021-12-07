import math

from Coders import intToBytes, bytesToInt
import socket


class CustomSocket(socket.socket):
    def __init__(self, bufferSize, *args, **kwargs):
        super(CustomSocket, self).__init__(*args, **kwargs)
        self.bufferSize = bufferSize

    def accept(self):
        fd, addr = super(CustomSocket, self)._accept()
        soc = CustomSocket(self.bufferSize, self.family, self.type, self.proto, fileno=fd)
        if soc.gettimeout() is None and self.gettimeout():
            soc.setblocking(True)
        return soc, addr

    def sendAllWithByteCount(self, data):
        dataToSend = bytearray(intToBytes(len(data)))
        dataToSend.extend(b'87654321')
        dataToSend.extend(data)
        super(CustomSocket, self).sendall(dataToSend)

    def recvAllWithByteCount(self):
        incomingData = super(CustomSocket, self).recv(self.bufferSize)
        indicator = b'87654321'
        length = bytearray()
        indicatorPos = 0
        dataPos = 0

        while (indicatorPos < len(indicator)) and (dataPos < len(incomingData)):
            if incomingData[dataPos] == indicator[indicatorPos]:
                indicatorPos += 1
            else:
                indicatorPos = 0
            length.append(incomingData[dataPos])
            dataPos += 1

        if not (indicatorPos < len(indicator)):
            lengthInt = bytesToInt(length[0:len(length)-8])
            if lengthInt > len(incomingData[dataPos:]):
                iteration = math.ceil((lengthInt + dataPos) / self.bufferSize) - 1
                incomingData = bytearray(incomingData[dataPos:])
                for i in range(0, iteration):
                    incomingData.extend(super(CustomSocket, self).recv(self.bufferSize))
            else:
                incomingData = incomingData[dataPos:]
        return incomingData

