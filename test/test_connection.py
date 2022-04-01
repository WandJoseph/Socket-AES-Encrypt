from os import urandom
import socket
import threading
import unittest
from project.AESCipher import AESCipher
import project.crypto

from project.client import Client


# Feature: Testing Client Communication
class TestConnection(unittest.TestCase):
    def setUp(self):
        self.server_port = 8888
        self.server_address = socket.gethostname()
        self.password = "P0"
        self.wrong_password = "P1"

    def test_client_connecting_to_the_server(self):
        """Scenario: Client connecting to the server
        Given the client, the server address and port
        When the client tries to connect to the server
        Then the client connects to the server
        """
        client = Client()
        # The client will send a error if cant connect
        client.connect((self.server_address, self.server_port))
        client.close()
        pass

    def test_client_authenticates_using_the_password(self):
        """Scenario: Client authenticates using the password
        Given the correct password, a server and a client connected to the server
        When the client send the form to authenticate in server
        Then the client is connected to the server and receives a AES Key
        """
        client = Client()
        client.connect((self.server_address, self.server_port))
        client.auth(self.password)
        received = client.receiveAesKey()
        self.assertTrue(received)
        client.close()
        pass

    def test_client_authenticates_using_the_wrong_password(self):
        """Scenario: Client authenticates using the wrong password
        Given a incorrect password, a server and a client connected to the server
        When the client send the form to authenticate in server
        Then client connection is closed by the server
        """

        client = Client()
        client.connect((self.server_address, self.server_port))
        client.auth(self.wrong_password)

        with self.assertRaises(Exception):
            client.receiveAesKey()

        client.close()
        pass

    def test_a_authenticated_client_send_a_encrtypted_hello(self):
        """Scenario: A Authenticated Client send a encrtypted 'hello'
        Given a aes key already registred in server, a server, a message
        When the client send the encrypted message
        Then server sends a response with 'hello to you too'
        """

        client = Client()
        client.connect((self.server_address, self.server_port))
        client.auth(self.password)
        received = client.receiveAesKey()
        self.assertTrue(received)
        client.sendEncrypted("hello")
        message = client.receiveEncrypted()
        self.assertEqual(message, "hello to you too")
        client.close()
        pass

    def test_a_authenticated_client_send_a_encrtypted_hello_with_a_wrong_key(self):
        """Scenario: A Authenticated Client send a encrtypted 'hello' with a wrong key
        Given a aes key already registred in server, a server, a message
        When the client send the encrypted message
        Then server sends a reply with the problem and diconnect the cli
        """
        client = Client()
        client.connect((self.server_address, self.server_port))
        client.auth(self.password)

        # Changing the client cypher decriptor
        received = client.receiveAesKey()
        self.assertTrue(received)

        aes = AESCipher(urandom(16))
        client.aes = aes

        client.sendEncrypted("hello")
        error_message = client.receive()
        self.assertEqual(error_message, 'Decryption failed!')
        client.close()

    def stopTestRun(self):
        pass


if __name__ == '__main__':
    unittest.main()
