# Feature: Testing AESCipher Encrypt

> **Scenario: Encripting a message with a random key**
> Given the random key, a message and the AESCipher
> When I encrypt the message using the AESCipher
> Then I should get a encrypted message

> **Scenario: Decrypting a message with a random key**
> Given the random key, a encrypted message and the AESCipher
> When I decrypt the message using the AESCipher
> Then I should get a original message

> **Scenario: Decrypting a message with a wrong key**
> Given the AESCipher for a random key, a AESCipher for a different key and a encrypted message
> When I decrypt the message using the AESCipher for the different key
> Then I should get a exception without decrypting the message
