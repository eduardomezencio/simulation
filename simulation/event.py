from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from simulation.id import generate_id

if TYPE_CHECKING:
    from simulation.patient import Patient
    from simulation.worker import Attendant, Doctor, Nurse


@dataclass
class Event:
    id: int = field(default_factory=generate_id)
    time: float = 0.0
    init_time: float = 0.0
    patient: Patient = None


@dataclass
class ArrivalEndEvent(Event):
    pass


@dataclass
class RegisterEndEvent(Event):
    attendant: Attendant = None


@dataclass
class ScreeningEndEvent(Event):
    nurse: Nurse = None


@dataclass
class ConsultationEndEvent(Event):
    doctor: Doctor = None


@dataclass
class ExamsEndEvent(Event):
    nurse: Nurse = None
