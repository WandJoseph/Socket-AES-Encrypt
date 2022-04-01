
import base64
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


def getPublicKey():
    with open('keys/public.pem', 'rb') as k:
        return k.read()


def getPrivateKey():
    with open('keys/private.pem', 'rb') as k:
        return k.read()


def encrypt(text: str):
    key = RSA.importKey(getPublicKey())
    cipher = Cipher_PKCS1_v1_5.new(key)
    return cipher.encrypt(text.encode())


def decrypt(encrypted_text: bytes):
    key = RSA.importKey(getPrivateKey())
    decipher = Cipher_PKCS1_v1_5.new(key)
    return decipher.decrypt(encrypted_text, None).decode()


def sign(message: str):
    digest = SHA256.new()
    digest.update(message.encode('utf-8'))

    private_key = RSA.importKey(getPrivateKey())

    # Sign the message
    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)

    # sig is bytes object, so convert to hex string.
    # (could convert using b64encode or any number of ways)
    return sig.hex()


def verify(message: str, sig):
    digest = SHA256.new()
    digest.update(message.encode('utf-8'))

    sig = bytes.fromhex(sig)

    public_key = RSA.importKey(getPublicKey())
    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(digest, sig)
    return verified
