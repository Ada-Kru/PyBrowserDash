from random import choice
from string import ascii_letters, digits


ID_LENGTH = 5
CHARS = ascii_letters + digits


def make_unused_id(current_ids):
    new_id = "".join(choice(CHARS) for _ in range(ID_LENGTH))
    return new_id if new_id not in current_ids else make_unused_id(current_ids)
