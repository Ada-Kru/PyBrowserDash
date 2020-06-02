from random import choice
from string import ascii_letters, digits


ID_LENGTH = 5
CHARS = ascii_letters + digits


def make_unused_id(current_ids):
    new_id = "".join(choice(CHARS) for _ in range(ID_LENGTH))
    return new_id if new_id not in current_ids else make_unused_id(current_ids)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
