from simulation.config import INSTANCE as CONFIG
from simulation.simulation import INSTANCE as SIMULATION


def main():
    with open('config.txt', 'r') as file:
        CONFIG.parse(file)

    from simulation.event import ArrivalEndEvent
    from simulation.patient import Patient

    SIMULATION.reset(lambda: ArrivalEndEvent(patient=Patient()))
    SIMULATION.run()


if __name__ == '__main__':
    main()
