from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from simulation.config import INSTANCE as CONFIG
from simulation.distribution import Distribution
from simulation.id import generate_id
from simulation.patient import Patient, Priority
from simulation.simulation import INSTANCE as SIMULATION
from simulation.worker import Attendant, Doctor, Nurse


@dataclass(eq=False)
class Event:
    distribution: ClassVar[Distribution] = None

    id: int = field(default_factory=generate_id)
    time: float = None
    init_time: float = None
    patient: Patient = None

    def __post_init__(self):
        if self.time is None:
            self.time = self.get_random_duration() + SIMULATION.time
            self.init_time = SIMULATION.time
        if self.patient is not None:
            self.patient.current_event = self

    @classmethod
    def get_random_duration(cls) -> float:
        return cls.distribution.get_value()

    def process(self):
        raise NotImplementedError()


@dataclass(eq=False)
class ArrivalEndEvent(Event):
    distribution: ClassVar[Distribution] = CONFIG.t_che

    def process(self):
        attendant = SIMULATION.get_idle_worker(Attendant)
        if attendant is not None:
            event = RegisterEndEvent(patient=self.patient, attendant=attendant)
            SIMULATION.push_event(event)
        else:
            SIMULATION.register_queue.push(self.patient)

        event = ArrivalEndEvent(patient=Patient())
        SIMULATION.push_event(event)


@dataclass(eq=False)
class RegisterEndEvent(Event):
    distribution: ClassVar[Distribution] = CONFIG.t_cad

    attendant: Attendant = None

    def __post_init__(self):
        super().__post_init__()
        if self.attendant is not None:
            self.attendant.current_event = self

    def process(self):
        if SIMULATION.register_queue:
            patient = SIMULATION.register_queue.pop()
            event = RegisterEndEvent(patient=patient, attendant=self.attendant)
            SIMULATION.push_event(event)
        else:
            self.attendant.current_event = None

        if self.patient.priority == Priority.EMERGENCY:
            doctor = SIMULATION.get_idle_worker(Doctor)
            if doctor is not None:
                event = ConsultationEndEvent(patient=self.patient,
                                             doctor=doctor)
                SIMULATION.push_event(event)
            else:
                SIMULATION.consultation_queue.push(self.patient)
        else:
            nurse = SIMULATION.get_idle_worker(Nurse)
            if nurse is not None:
                event = ScreeningEndEvent(patient=self.patient, nurse=nurse)
                SIMULATION.push_event(event)
            else:
                SIMULATION.screening_queue.push(self.patient)


@dataclass(eq=False)
class ScreeningEndEvent(Event):
    distribution: ClassVar[Distribution] = CONFIG.t_tri

    nurse: Nurse = None

    def __post_init__(self):
        super().__post_init__()
        if self.nurse is not None:
            self.nurse.current_event = self

    def process(self):
        if SIMULATION.screening_queue:
            patient = SIMULATION.screening_queue.pop()
            event = ScreeningEndEvent(patient=patient, nurse=self.nurse)
            SIMULATION.push_event(event)
        elif SIMULATION.exams_queue:
            patient = SIMULATION.exams_queue.pop()
            event = ExamsEndEvent(patient=patient, nurse=self.nurse)
            SIMULATION.push_event(event)
        else:
            self.nurse.current_event = None

        doctor = SIMULATION.get_idle_worker(Doctor)
        if doctor is not None:
            event = ConsultationEndEvent(patient=self.patient, doctor=doctor)
            SIMULATION.push_event(event)
        else:
            SIMULATION.consultation_queue.push(self.patient)


@dataclass(eq=False)
class ConsultationEndEvent(Event):
    distribution: ClassVar[Distribution] = CONFIG.t_ate

    doctor: Doctor = None

    def __post_init__(self):
        super().__post_init__()
        if self.doctor is not None:
            self.doctor.current_event = self

    def process(self):
        if SIMULATION.consultation_queue:
            patient = SIMULATION.consultation_queue.pop()
            event = ConsultationEndEvent(patient=patient, doctor=self.doctor)
            SIMULATION.push_event(event)
        else:
            self.doctor.current_event = None

        if self.patient.need_exams:
            nurse = SIMULATION.get_idle_worker(Nurse)
            if nurse is not None:
                event = ExamsEndEvent(patient=self.patient, nurse=nurse)
                SIMULATION.push_event(event)
            else:
                SIMULATION.exams_queue.push(self.patient)
        else:
            self.patient.current_event = None


@dataclass(eq=False)
class ExamsEndEvent(Event):
    distribution: ClassVar[Distribution] = CONFIG.t_exa

    nurse: Nurse = None

    def __post_init__(self):
        super().__post_init__()
        if self.nurse is not None:
            self.nurse.current_event = self

    def process(self):
        if SIMULATION.exams_queue:
            patient = SIMULATION.exams_queue.pop()
            event = ExamsEndEvent(patient=patient, nurse=self.nurse)
            SIMULATION.push_event(event)
        elif SIMULATION.screening_queue:
            patient = SIMULATION.screening_queue.pop()
            event = ScreeningEndEvent(patient=patient, nurse=self.nurse)
            SIMULATION.push_event(event)
        else:
            self.nurse.current_event = None
        self.patient.current_event = None
