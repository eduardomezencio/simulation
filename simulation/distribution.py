from random import (betavariate, expovariate, gammavariate, lognormvariate,
                    normalvariate, paretovariate, triangular, uniform,
                    weibullvariate)
from typing import Callable

FUNCTIONS = {
    'BET': (betavariate, 2),
    'EXP': (expovariate, 1),
    'GAM': (gammavariate, 2),
    'LOG': (lognormvariate, 2),
    'NOR': (normalvariate, 2),
    'PAR': (paretovariate, 1),
    'TRI': (triangular, 3),
    'UNI': (uniform, 2),
    'WEI': (weibullvariate, 2)
}


class Distribution:
    def __init__(self, function: Callable[..., float], *args):
        self.function = function
        self.params = args

    def get_value(self) -> float:
        return self.function(*self.params)


def distribution_factory(name: str, *args) -> Distribution:
    function, num_args = FUNCTIONS[name]
    return Distribution(function, *(args[:num_args]))
