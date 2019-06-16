from simulation.config import INSTANCE as CONFIG
from simulation.simulation import INSTANCE as SIMULATION
from simulation.stats import Stats


def main():
    with open('config.txt', 'r') as file:
        CONFIG.parse(file)

    from simulation.event import ArrivalEndEvent

    SIMULATION.reset(lambda: ArrivalEndEvent(patient=SIMULATION.new_patient()))
    SIMULATION.run()
    print('\n'.join(map(str, SIMULATION.event_log)))
    print(Stats.calculate(SIMULATION))


if __name__ == '__main__':
    main()
