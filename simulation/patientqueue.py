from simulation.config import INSTANCE as CONFIG
from simulation.patient import Patient, Priority
from simulation.random import roulette


class PatientQueue:
    def __init__(self):
        self._len = 0
        self.queues = tuple([] for _ in CONFIG.p_que)

    def push(self, patient: Patient):
        self.queues[patient.priority.value - 1].append(patient)
        self._len += 1

    def pop(self) -> Patient:
        if all(not q for q in self.queues):
            raise Exception('Empty queue')
        weights = CONFIG.p_que
        values = [p for p in Priority]
        while True:
            selected = roulette(weights, values).value - 1
            if self.queues[selected]:
                self._len -= 1
                return self.queues[selected].pop()

    def __len__(self):
        return self._len
