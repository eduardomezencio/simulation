from itertools import accumulate
from random import random
from typing import Iterable, TypeVar

T = TypeVar('T')


def roulette(weights: Iterable[float], values: Iterable[T]) -> T:
    result = random() * sum(weights)
    for weight, value in zip(accumulate(weights), values):
        if result <= weight:
            return value
    raise ValueError('Invalid weights')
