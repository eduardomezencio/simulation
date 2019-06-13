from itertools import count

ID_COUNT = count(1)


def generate_id():
    return next(ID_COUNT)
