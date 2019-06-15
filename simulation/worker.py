from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from simulation.id import generate_id

if TYPE_CHECKING:
    from simulation.event import Event


@dataclass(eq=False)
class Worker:

    id: int = field(default_factory=generate_id)
    total_idle_time: float = 0.0
    current_event: Event = None
    last_event: Event = None

    @property
    def free(self):
        return self.current_event is None


class Attendant(Worker):
    pass


class Nurse(Worker):
    pass


class Doctor(Worker):
    pass
