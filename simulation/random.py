from itertools import accumulate
from random import random
from typing import Tuple


def roulette(weights: Tuple[float], values: tuple):
    result = random()
    for weight, value in zip(accumulate(weights), values):
        if result <= weight:
            return value
    raise ValueError('Invalid weights')
