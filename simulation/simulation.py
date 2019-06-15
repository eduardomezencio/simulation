from __future__ import annotations

from typing import Callable, List, Set, Type, TYPE_CHECKING

from simulation.config import INSTANCE as CONFIG
from simulation.patientqueue import PatientQueue
from simulation.pqueue import PQueue
from simulation.worker import Attendant, Doctor, Nurse, Worker

if TYPE_CHECKING:
    from simulation.event import Event


class Simulation:
    event_queue: PQueue[Event]
    event_log: List[Event]
    initial_event_factory: Callable[[], Event]
    register_queue: PatientQueue
    screening_queue: PatientQueue
    consultation_queue: PatientQueue
    exams_queue: PatientQueue
    workers: Set[Worker]
    _time: float

    @property
    def time(self):
        return self._time

    def reset(self, initial_event_factory: Callable[[], Event]):
        self.initial_event_factory = initial_event_factory

        self._time = 0.0
        self.register_queue = PatientQueue()
        self.screening_queue = PatientQueue()
        self.consultation_queue = PatientQueue()
        self.exams_queue = PatientQueue()

        self.workers = set()
        self._create_workers()

        self.event_log = []
        self.event_queue = PQueue()
        self.push_event(self.initial_event_factory())

    def push_event(self, event: Event):
        self.event_queue.push(event, event.time)

    def get_idle_worker(self, type_: Type[Worker]) -> Worker:
        return next(
            filter(lambda w: isinstance(w, type_) and w.free, self.workers),
            None)

    def run(self):
        for event, time in self.event_queue:
            if time > CONFIG.t_tts:
                break
            self._time = time
            event.process()
            self.event_log.append(event)
        print(self.event_log)

    def _create_workers(self):
        for _ in range(CONFIG.q_atd):
            self.workers.add(Attendant())
        for _ in range(CONFIG.q_enf):
            self.workers.add(Nurse())
        for _ in range(CONFIG.q_med):
            self.workers.add(Doctor())


INSTANCE = Simulation()
