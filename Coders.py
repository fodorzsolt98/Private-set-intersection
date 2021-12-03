from base64 import b64encode, b64decode
import json


def encodeBase64(text):
    return b64encode(text).decode('utf-8')


def decodeBase64(text):
    return b64decode(text.encode('utf-8'))


def jsonToBytes(message):
    return json.dumps(message).encode('utf-8')


def bytesToJson(message):
    return json.loads(message.decode('utf-8'))


def intToBytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def bytesToInt(b):
    return int.from_bytes(b, 'big')

