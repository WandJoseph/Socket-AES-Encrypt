import os
import unittest

from AESCipher import AESCipher
from utils import random_string

"""
    Feature: Testing AESCipher Encrypt
"""


class TestAESModule(unittest.TestCase):

    def test_encrypt(self):
        """
        Scenario: Encripting a message with a random key
        Given the random key, a message and the AESCipher
        When I encrypt the message using the AESCipher
        Then I should get a encrypted message
        """
        random_key = os.urandom(16)
        message = random_string()

        aes = AESCipher(random_key)
        encrypted_message = aes.encrypt(message)
        self.assertNotEqual(message, encrypted_message)
        pass

    def test_decrypt(self):
        """
        Scenario: Decrypting a message with a random key
        Given the random key, a encrypted message and the AESCipher
        When I decrypt the message using the AESCipher
        Then I should get a original message
        """
        random_key = os.urandom(16)
        message = random_string()
        aes_key1 = AESCipher(random_key)
        encrypted_message = aes_key1.encrypt(message)
        decrypted_message = aes_key1.decrypt(encrypted_message)
        self.assertEqual(message, decrypted_message)

    def test_decrypt_another_key(self):
        """
        Scenario: Decrypting a message with a wrong key
        Given the AESCipher for a random key, a AESCipher for a different key and a encrypted message
        When I decrypt the message using the AESCipher for the different key
        Then I should get a exception without decrypting the message
        """

        random_key1 = os.urandom(16)
        random_key2 = os.urandom(16)
        message = random_string()
        aes_key1 = AESCipher(random_key1)
        aes_key2 = AESCipher(random_key2)
        encrypted_message_key1 = aes_key1.encrypt(message)
        with self.assertRaises(Exception):
            aes_key2.decrypt(encrypted_message_key1)


if __name__ == '__main__':
    unittest.main()
