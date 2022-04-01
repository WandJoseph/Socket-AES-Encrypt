import base64
import socket
import os
import threading
import hashlib
from json import loads as json_load, dumps as json_dump

from pyrsistent import b
import crypto
from AESCipher import AESCipher


class Server(socket.socket):
    password = 'P0'
    keys = {}

    def __init__(self, port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.bind((socket.gethostname(), port))
        self.listen(5)
        self.acceptConnections()
        self.close()

    def acceptConnections(self):
        print(f'[*] Server started on port {self.port}')
        while True:
            try:
                client, address = self.accept()
                print(f"Client connected from {address}")
                # DECRYPT USING PRIVATE KEY TO CHECK PASSWORD
                self.auth(client, address)
                self.receiveEncrypted(client, address)
                # THE SERVER WILL SEND A RANDOMLY GENERATED AES KEY AS KEY + SIGNATURE (SIGNED WITH PRIVATE KEY) TO THE CLIENT
            except Exception as e:
                print(e)
                client.close()
                pass

    def auth(self, client: socket.socket, address):
        message_bytes: bytes = client.recv(1024)
        json_string = crypto.decrypt(message_bytes)
        payload = json_load(json_string)
        if payload['password'] != self.password:
            print("\tInvalid password authentication\n")
            client.close()
            return
        print("\tClient Authenticated!\n")
        self.sendAESKey(client, address)

    def sendAESKey(self, client, address):
        key = os.urandom(16).hex()
        payload = {
            'aes_key': key,
            'signature': crypto.sign(key)
        }
        message = json_dump(payload).encode("utf-8")
        print(f"\tSending New Random AES_KEY: {key}\n")
        client.send(message)
        self.keys[address] = key

    def receiveEncrypted(self, client, address):
        message_bytes: bytes = client.recv(1024)
        message_encrypted = message_bytes.decode("utf-8")
        print(f"\tReceived encrypted: {message_encrypted}")
        try:
            aes = AESCipher(bytes.fromhex(self.keys[address]))
            message = aes.decrypt(message_encrypted)
            print(f"\tMessage decrypted: {message}\n")
            if(message == "Hello"):
                reply = "hello to you too"
                self.sendEncrypted(client, address, reply)
        except KeyError:
            print("\tClient not authenticated")
            client.send(b("Client not authenticated"))
            client.close()
            pass
        except Exception as e:
            print("\tError in message decryption")
            client.send("Decryption failed!".encode("utf-8"))
            client.close()
            pass

    def sendEncrypted(self, client, address, message: str):
        aes_key = self.keys[address]
        aes = AESCipher(bytes.fromhex(aes_key))
        message_encrypted = aes.encrypt(message)
        message_bytes = message_encrypted.encode("utf-8")
        print(f"\tSending \"{message}\"\n\tencrypted: {message_encrypted}\n")
        client.send(message_bytes)


server = Server(8888)
