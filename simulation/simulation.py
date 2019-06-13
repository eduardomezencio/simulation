from simulation.patientqueue import PatientQueue


class Simulation:
    register_queue: PatientQueue
    screening_queue: PatientQueue
    consultation_queue: PatientQueue
    exams_queue: PatientQueue

    def __init__(self):
        pass
