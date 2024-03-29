from itertools import chain
from typing import Iterator

from simulation.config import INSTANCE as CONFIG
from simulation.patient import Patient, Priority
from simulation.random import roulette


class PatientQueue:
    def __init__(self):
        self._count = 0
        self._len = 0
        self._max_len = 0
        self._len_time = 0.0
        self._entered = {}
        self._max_waiting_time = 0.0
        self._total_waiting_time = 0.0
        self.queues = tuple([] for _ in CONFIG.p_que)

    @property
    def total_patient_count(self) -> int:
        return self._count

    @property
    def max_waiting_time(self) -> float:
        return self._max_waiting_time

    @property
    def total_waiting_time(self) -> float:
        return self._total_waiting_time

    @property
    def max_len(self) -> int:
        return self._max_len

    def push(self, patient: Patient, time: float):
        patient.current_event = None
        self.queues[patient.priority.value - 1].append(patient)
        self._count += 1
        self._len += 1
        self._max_len = max(self._len, self._max_len)
        self._entered[patient] = time

    def skip(self):
        self._count += 1

    def pop(self, time: float) -> Patient:
        weights = [p for p, q in zip(CONFIG.p_que, self.queues) if q]
        values = [p for p, q in zip(Priority, self.queues) if q]
        if not weights:
            raise Exception('Empty queue')
        patient = None
        while patient is None:
            selected = roulette(weights, values).value - 1
            if self.queues[selected]:
                self._len -= 1
                patient = self.queues[selected].pop()
        waiting = time - self._entered[patient]
        if self._max_waiting_time < waiting:
            self._max_waiting_time = waiting
        self._total_waiting_time += waiting
        if patient.max_waiting_time < waiting:
            patient.max_waiting_time = waiting
        del self._entered[patient]
        return patient

    def peek_all(self) -> Iterator[Patient]:
        yield from chain.from_iterable(self.queues)

    def update_stats(self, delta: float):
        self._len_time += self._len * delta
        for patient in self.peek_all():
            patient.total_waiting_time += delta

    def mean_len(self, total_time: float) -> float:
        return self._len_time / total_time

    def mean_waiting_time(self) -> float:
        return self._total_waiting_time / self._count

    def __len__(self):
        return self._len

    def __bool__(self):
        return bool(self._len)
