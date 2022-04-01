import socket
from project.AESCipher import AESCipher

import project.crypto as crypto
from json import dumps as json_dump, loads as json_load


class Client(socket.socket):
    aes_key: str = None
    aes: AESCipher = None

    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def auth(self, password):
        payload = {
            'password': password
        }
        payload_str = json_dump(payload)
        encrypted_payload = crypto.encrypt(payload_str)
        print(f"\nSending Encrypted Auth\n")
        self.send(encrypted_payload)

    def receiveAesKey(self):
        payload_encoded = self.recv(1024)
        payload: dict = json_load(payload_encoded.decode("utf-8"))
        aes_key = payload.get('aes_key')
        signature = payload.get('signature')
        print(f"AES Key Received: {aes_key}\nSignature: {signature}\n")
        if not crypto.verify(aes_key, signature):
            print("Invalid Signature")
            self.close()
            return False
        print("AES Key Verified!\n")
        self.aes_key = bytes.fromhex(aes_key)
        self.aes = AESCipher(self.aes_key)
        return True

    def sendEncrypted(self, message: str):
        encrypted = self.aes.encrypt("Hello")
        print(f"Sending: {message}, encrypted: {encrypted}")
        self.send(encrypted.encode("utf-8"))

    def receiveEncrypted(self):
        message_encrypted = self.receive()
        print(f"Received encrypted Message: {message_encrypted}")
        try:
            message = self.aes.decrypt(message_encrypted)
            print(f"Message Decrypted: {message}!\n")
            return message
        except Exception as e:
            print("Fail to decrypt message")
            print(e)
            self.close()
            return

    def receive(self):
        message_bytes: bytes = self.recv(1024)
        message = message_bytes.decode("utf-8")
        return message
