import random


def generate_random_code(length):
    pl = random.sample(['1', '2', '3', '4', '5', '6',
                        '7', '8', '9', '0'], length)
    code = ''.join(pl)
    return code
