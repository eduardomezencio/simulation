from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import accumulate
from random import randrange, random

from simulation.config import INSTANCE as CONFIG
from simulation.event import Event
from simulation.id import generate_id


class Priority(Enum):

    NON_URGENT = 1
    LESS_URGENT = 2
    URGENT = 3
    VERY_URGENT = 4
    EMERGENCY = 5

    def weight(self, table=CONFIG.p_pri) -> int:
        return table[self.value - 1]

    @staticmethod
    def get_random() -> Priority:
        acc = accumulate(p.weight() for p in Priority)
        total = acc[-1]
        rand = randrange(total)
        for index, value in enumerate(acc):
            if rand < value:
                return Priority(index + 1)


def get_random_need_exams():
    return random() < CONFIG.p_pro


@dataclass
class Patient:

    id: int = field(default_factory=generate_id)
    priority: Priority = field(default_factory=Priority.get_random)
    need_exams: bool = field(default_factory=get_random_need_exams)
    total_waiting_time: float = 0.0
    current_event: Event = None
    last_event: Event = None
