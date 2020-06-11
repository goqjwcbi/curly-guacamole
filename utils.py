import random
import string


def gen_id():
    return "".join(random.choice(string.ascii_letters) for i in range(8))
