from __future__ import annotations

from typing import Callable, Iterator, List, Set, Tuple, Type, TYPE_CHECKING

from simulation.config import INSTANCE as CONFIG
from simulation.patient import Patient
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
    patients: Set[Patient]
    workers: Set[Worker]
    _time: float

    @property
    def queues(self) -> Tuple[PatientQueue]:
        return (self.register_queue, self.screening_queue,
                self.consultation_queue, self.exams_queue)

    @property
    def named_queues(self) -> Tuple[Tuple[str, PatientQueue]]:
        return tuple((n, getattr(self, n)) for n in (
            'register_queue', 'screening_queue',
            'consultation_queue', 'exams_queue'))

    @property
    def time(self) -> float:
        return self._time

    def reset(self, initial_event_factory: Callable[[], Event]):
        self.initial_event_factory = initial_event_factory

        self._time = 0.0
        self.register_queue = PatientQueue()
        self.screening_queue = PatientQueue()
        self.consultation_queue = PatientQueue()
        self.exams_queue = PatientQueue()

        self.patients = set()
        self.workers = set()
        self._create_workers()

        self.event_log = []
        self.event_queue = PQueue()
        self.push_event(self.initial_event_factory())

    def push_event(self, event: Event):
        self.event_queue.push(event, event.time)

    def get_idle_workers(self, type_: Type[Worker]) -> Iterator[Worker]:
        yield from filter(lambda w: isinstance(w, type_) and w.free,
                          self.workers)

    def get_idle_worker(self, type_: Type[Worker]) -> Worker:
        return next(self.get_idle_workers(type_), None)

    def run(self):
        for event, time in self.event_queue:
            if time > CONFIG.t_tts:
                break
            delta = time - self._time
            self._time = time
            self._update_stats(delta)
            event.process()
            self.event_log.append(event)

    def new_patient(self) -> Patient:
        patient = Patient()
        self.patients.add(patient)
        return patient

    def _create_workers(self):
        for _ in range(CONFIG.q_atd):
            self.workers.add(Attendant())
        for _ in range(CONFIG.q_enf):
            self.workers.add(Nurse())
        for _ in range(CONFIG.q_med):
            self.workers.add(Doctor())

    def _update_stats(self, delta: float):
        for queue in self.queues:
            queue.update_stats(delta)
        for worker in self.get_idle_workers(Worker):
            worker.total_idle_time += delta


INSTANCE = Simulation()
