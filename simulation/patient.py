from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import accumulate
from random import random
from typing import TYPE_CHECKING

from simulation.config import INSTANCE as CONFIG
from simulation.id import generate_id

if TYPE_CHECKING:
    from simulation.event import Event


class Priority(Enum):

    NON_URGENT = 1
    LESS_URGENT = 2
    URGENT = 3
    VERY_URGENT = 4
    EMERGENCY = 5

    @property
    def weight(self) -> int:
        return CONFIG.p_pri[self.value - 1]

    @staticmethod
    def get_random() -> Priority:
        acc = list(accumulate(p.weight for p in Priority))
        total = acc[-1]
        rand = random() * total
        for index, value in enumerate(acc):
            if rand < value:
                return Priority(index + 1)


def get_random_need_exams():
    return random() < CONFIG.p_pro


@dataclass(eq=False)
class Patient:

    id: int = field(default_factory=generate_id)
    priority: Priority = field(default_factory=Priority.get_random)
    need_exams: bool = field(default_factory=get_random_need_exams)
    total_waiting_time: float = 0.0
    _current_event: Event = field(init=False, default=None)
    _last_event: Event = field(init=False, default=None)

    @property
    def current_event(self):
        return self._current_event

    @current_event.setter
    def current_event(self, value):
        if self._current_event is not None:
            self._last_event = self._current_event
        self._current_event = value

    @property
    def last_event(self):
        return self._last_event

    def __str__(self):
        return (f'{type(self).__name__}({self.id}, {self.priority.name}'
                f'{", exams" if self.need_exams else ""})')
