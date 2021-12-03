from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Coders import encodeBase64, decodeBase64

class MessageCipher:
    def __init__(self, pem=None):
        if pem:
            self.asymmetricKey = RSA.importKey(pem)
        else:
            self.asymmetricKey = RSA.generate(2048)
        self.asymmetricCipher = PKCS1_OAEP.new(self.asymmetricKey)

    def getSessionCipherSet(self):
        header = get_random_bytes(16)
        key = get_random_bytes(32)
        cipher = AES.new(key, AES.MODE_EAX)
        cipher.update(header)
        return {
            'header': encodeBase64(header),
            'key': encodeBase64(key),
            'cipher': cipher
        }

    def setSessionCipher(self, header, key, nonce):
        cipher = AES.new(decodeBase64(key), AES.MODE_EAX, nonce=decodeBase64(nonce))
        cipher.update(decodeBase64(header))
        return cipher

    def symmetricEncryptionWithSessionkey(self, cipher, data):
        ctext, tag = cipher.encrypt_and_digest(data)
        return {
            'cipherText': encodeBase64(ctext),
            'tag': encodeBase64(tag),
            'nonce': encodeBase64(cipher.nonce)
        }

    def symmetricDecrytionWithSessionkey(self, cipher, data, tag):
        try:
            return cipher.decrypt_and_verify(decodeBase64(data), decodeBase64(tag))
        except (ValueError, KeyError) as exc:
            return None

    def asymmetricEncryption(self, data):
        return encodeBase64(self.asymmetricCipher.encrypt(data))

    def asymmetricDecryption(self, data):
        return self.asymmetricCipher.decrypt(decodeBase64(data))
