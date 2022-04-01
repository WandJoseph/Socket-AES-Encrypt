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

# Feature: Testing Client Communication

> **Scenario: Client connecting to the server**
> Given the client, the server address and port
> When the client tries to connect to the server
> Then the client connects to the server

> **Scenario: Client authenticates using the password**
> Given the correct password, a server and a client connected to the server
> When the client send the form to authenticate in server
> Then the client is connected to the server and receives a AES Key

> **Scenario: Client authenticates using the wrong password**
> Given a incorrect password, a server and a client connected to the server
> When the client send the form to authenticate in server
> Then client connection is closed after a message with the problem

> **Scenario: A Authenticated Client send a encrtypted 'hello'**
> Given a aes key already registred in server, a server, a message
> When the client send the encrypted message
> Then server sends a response with 'hello to you too'

> **Scenario: A Authenticated Client send a encrtypted 'hello' with a wrong key**
> Given a aes key already registred in server, a server, a message
> When the client send the encrypted message
> Then server sends a reply with the problem and diconnect the cli
