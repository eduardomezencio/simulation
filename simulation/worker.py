from __future__ import annotations

from dataclasses import dataclass, field

from simulation.event import Event
from simulation.id import generate_id


@dataclass
class Worker:

    id: int = field(default_factory=generate_id)
    occupied: bool = False
    total_idle_time: float = 0.0
    current_event: Event = None
    last_event: Event = None


class Attendant(Worker):
    pass


class Nurse(Worker):
    pass


class Doctor(Worker):
    pass
