from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

from simulation.patient import Priority

if TYPE_CHECKING:
    from simulation.simulation import Simulation


@dataclass
class Stats:
    total_simulation_time: float
    total_patients: int
    patients_by_priority: Dict[str, int]
    total_workers: int
    workers_by_type: Dict[str, int]
    mean_waiting_time: float
    mean_waiting_time_by_priority: Dict[Priority, float]
    mean_waiting_time_by_queue: Dict[str, float]
    mean_idle_time: float
    mean_idle_time_by_type: Dict[str, float]
    max_queue_len: int
    max_queue_len_by_queue: Dict[str, int]
    mean_queue_len: float
    mean_queue_len_by_queue: Dict[str, float]

    @staticmethod
    def calculate(simulation: Simulation) -> Stats:
        total_simulation_time = simulation.time
        total_patients = len(simulation.patients)
        patients_by_priority = defaultdict(int)
        mean_waiting_time = 0.0
        mean_waiting_time_by_priority = defaultdict(float)
        for patient in simulation.patients:
            patients_by_priority[patient.priority.name] += 1
            mean_waiting_time += patient.total_waiting_time
            mean_waiting_time_by_priority[patient.priority] += \
                patient.total_waiting_time
        mean_waiting_time /= total_patients
        for priority in Priority:
            mean_waiting_time_by_priority[priority] /= \
                patients_by_priority[priority.name]

        total_workers = len(simulation.workers)
        workers_by_type = defaultdict(int)
        mean_idle_time = 0.0
        mean_idle_time_by_type = defaultdict(float)
        for worker in simulation.workers:
            workers_by_type[type(worker).__name__] += 1
            mean_idle_time += worker.total_idle_time
            mean_idle_time_by_type[type(worker).__name__] += \
                worker.total_idle_time
        mean_idle_time /= total_workers
        for type_ in mean_idle_time_by_type.keys():
            mean_idle_time_by_type[type_] /= workers_by_type[type_]

        max_queue_len_by_queue = {}
        mean_queue_len_by_queue = {}
        mean_waiting_time_by_queue = {}
        for name, queue in simulation.named_queues:
            max_queue_len_by_queue[name] = queue.max_len
            mean_queue_len_by_queue[name] = queue.mean_len(simulation.time)
            mean_waiting_time_by_queue[name] = queue.mean_waiting_time()
        max_queue_len = max(max_queue_len_by_queue.values())
        mean_queue_len = (sum(mean_queue_len_by_queue.values()) /
                          len(mean_queue_len_by_queue))

        return Stats(total_simulation_time, total_patients,
                     dict(patients_by_priority), total_workers,
                     dict(workers_by_type), mean_waiting_time,
                     dict(mean_waiting_time_by_priority),
                     mean_waiting_time_by_queue, mean_idle_time,
                     dict(mean_idle_time_by_type), max_queue_len,
                     max_queue_len_by_queue, mean_queue_len,
                     mean_queue_len_by_queue)

    def __str__(self):
        return '\n'.join(f'\n{k}:\n    {str(v)}'
                         for k, v in self.__dict__.items())
