from random import choice
from string import ascii_uppercase, digits


def random_string(size=10):
    return ''.join(choice(ascii_uppercase + digits)
                   for _ in range(size))
