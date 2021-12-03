from Coders import jsonToBytes, bytesToJson


class Client:
    def __init__(self, connection, localCipher, partnerCipher):
        self.connection = connection
        self.localCipher = localCipher
        self.partnerCipher = partnerCipher

    def sendData(self, data):
        symmetricCipherSet = self.localCipher.getSessionCipherSet()
        symmetricEncryptionSet = self.localCipher.symmetricEncryptionWithSessionkey(symmetricCipherSet['cipher'], data)
        header = symmetricCipherSet
        header.update(symmetricEncryptionSet)
        header.pop('cipher', None)
        header.pop('cipherText', None)
        jsonToSend = {
            'head': self.partnerCipher.asymmetricEncryption(jsonToBytes(header)),
            'data': symmetricEncryptionSet['cipherText']
        }
        self.connection.sendAllWithByteCount(jsonToBytes(jsonToSend))

    def receiveData(self):
        incomingData = bytesToJson(self.connection.recvAllWithByteCount())
        head = bytesToJson(self.localCipher.asymmetricDecryption(incomingData['head']))
        sessionCipher = self.partnerCipher.setSessionCipher(head['header'], head['key'], head['nonce'])
        return self.partnerCipher.symmetricDecrytionWithSessionkey(sessionCipher, incomingData['data'], head['tag'])

    def sendText(self, message):
        self.sendData(message.encode('utf-8'))

    def receiveText(self):
        return self.receiveData().decode('utf-8')

    def bye(self):
        self.connection.close()
