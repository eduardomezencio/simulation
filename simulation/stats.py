from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import ClassVar, Dict, TYPE_CHECKING

from simulation.patient import Priority

if TYPE_CHECKING:
    from simulation.simulation import Simulation

DEFAULT_CSV_SEPARATOR = '\t'


@dataclass
class Stats:
    total_simulation_time: float
    total_patients: int
    patients_by_priority: Dict[int, int]
    total_workers: int
    workers_by_type: Dict[str, int]
    max_waiting_time: float
    max_waiting_time_by_priority: Dict[int, float]
    max_waiting_time_by_queue: Dict[str, float]
    mean_waiting_time: float
    mean_waiting_time_by_priority: Dict[int, float]
    mean_waiting_time_by_queue: Dict[str, float]
    mean_idle_time: float
    mean_idle_time_by_type: Dict[str, float]
    max_queue_len: int
    max_queue_len_by_queue: Dict[str, int]
    mean_queue_len: float
    mean_queue_len_by_queue: Dict[str, float]

    CSV_COLUMNS: ClassVar = (
        'mean_idle_time', 'mean_idle_time_by_type', 'mean_waiting_time',
        'mean_waiting_time_by_priority', 'mean_waiting_time_by_queue',
        'mean_queue_len', 'mean_queue_len_by_queue', 'max_waiting_time',
        'max_waiting_time_by_priority', 'max_waiting_time_by_queue',
        'max_queue_len', 'max_queue_len_by_queue')
    PRIORITIES: ClassVar = (1, 2, 3, 4, 5)
    QUEUES: ClassVar = ('register_queue', 'screening_queue',
                        'consultation_queue', 'exams_queue')
    WORKERS: ClassVar = ('Attendant', 'Nurse', 'Doctor')
    ORDER: ClassVar = (None, WORKERS, None, PRIORITIES, QUEUES, None, QUEUES,
                       None, PRIORITIES, QUEUES, None, QUEUES)

    @staticmethod
    def calculate(simulation: Simulation) -> Stats:
        total_simulation_time = simulation.time
        total_patients = len(simulation.patients)
        patients_by_priority = defaultdict(int)
        max_waiting_time_by_priority = defaultdict(float)
        mean_waiting_time = 0.0
        mean_waiting_time_by_priority = defaultdict(float)
        for patient in simulation.patients:
            patients_by_priority[patient.priority.value] += 1
            max_waiting_time_by_priority[patient.priority.value] = \
                max(max_waiting_time_by_priority[patient.priority.value],
                    patient.max_waiting_time)
            mean_waiting_time += patient.total_waiting_time
            mean_waiting_time_by_priority[patient.priority.value] += \
                patient.total_waiting_time
        mean_waiting_time /= total_patients
        for priority in Priority:
            mean_waiting_time_by_priority[priority.value] /= \
                patients_by_priority[priority.value]

        total_workers = len(simulation.workers)
        workers_by_type = defaultdict(int)
        mean_idle_time = 0.0
        mean_idle_time_by_type = defaultdict(float)
        for worker in simulation.workers:
            workers_by_type[type(worker).__name__] += 1
            mean_idle_time += worker.total_idle_time
            mean_idle_time_by_type[type(worker).__name__] += \
                worker.total_idle_time
        mean_idle_time /= total_workers * simulation.time
        for type_ in mean_idle_time_by_type.keys():
            mean_idle_time_by_type[type_] /= \
                workers_by_type[type_] * simulation.time

        max_queue_len_by_queue = {}
        mean_queue_len_by_queue = {}
        max_waiting_time_by_queue = {}
        mean_waiting_time_by_queue = {}
        for name, queue in simulation.named_queues:
            max_queue_len_by_queue[name] = queue.max_len
            mean_queue_len_by_queue[name] = queue.mean_len(simulation.time)
            max_waiting_time_by_queue[name] = queue.max_waiting_time
            mean_waiting_time_by_queue[name] = queue.mean_waiting_time()
        max_queue_len = max(max_queue_len_by_queue.values())
        mean_queue_len = (sum(mean_queue_len_by_queue.values()) /
                          len(mean_queue_len_by_queue))
        max_waiting_time = max(max_waiting_time_by_queue.values())

        return Stats(total_simulation_time, total_patients,
                     dict(patients_by_priority), total_workers,
                     dict(workers_by_type), max_waiting_time,
                     max_waiting_time_by_priority, max_waiting_time_by_queue,
                     mean_waiting_time, dict(mean_waiting_time_by_priority),
                     mean_waiting_time_by_queue, mean_idle_time,
                     dict(mean_idle_time_by_type), max_queue_len,
                     max_queue_len_by_queue, mean_queue_len,
                     mean_queue_len_by_queue)

    @classmethod
    def get_csv_header(cls, separator=DEFAULT_CSV_SEPARATOR) -> str:
        def expand(value: str) -> str:
            if value.endswith('_by_priority'):
                return separator.join(value.replace('_by_priority', f'-{p}')
                                      for p in cls.PRIORITIES)
            if value.endswith('_by_queue'):
                return separator.join(value.replace('_by_queue', f'-{q}')
                                      for q in cls.QUEUES)
            if value.endswith('_by_type'):
                return separator.join(value.replace('_by_type', f'-{w}')
                                      for w in cls.WORKERS)
            return str(value)

        return separator.join(expand(c) for c in cls.CSV_COLUMNS)

    def get_csv(self, separator=DEFAULT_CSV_SEPARATOR) -> str:
        def format_(value) -> str:
            if isinstance(value, int):
                return str(value)
            return format(value, '.2f')

        def expand(value, order) -> str:
            if order is None:
                return format_(value)
            return separator.join(format_(value[o]) for o in order)

        return separator.join(expand(self.__dict__[v], o)
                              for v, o in zip(Stats.CSV_COLUMNS, Stats.ORDER))

    def __str__(self):
        def format_(value):
            if isinstance(value, dict):
                return (f'{k}: {value[k]}' for k in sorted(value.keys()))
            return (str(value),)

        indent = '\n    '
        return '\n'.join(f'\n{k}:{indent}{indent.join(format_(v))}'
                         for k, v in self.__dict__.items())
