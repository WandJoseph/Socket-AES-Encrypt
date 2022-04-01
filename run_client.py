

import socket
from project.client import Client


def main():
    server_port = 8888
    server_address = socket.gethostname()
    password = "P0"

    client = Client()
    client.connect((server_address, server_port))
    client.auth(password)

    client.receiveAesKey()
    client.sendEncrypted("hello")
    client.receiveEncrypted()
    client.close()


if __name__ == '__main__':
    main()
