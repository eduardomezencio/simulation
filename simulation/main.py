import sys

from simulation.config import INSTANCE as CONFIG
from simulation.simulation import INSTANCE as SIMULATION
from simulation.stats import Stats


def main():
    if '--header' in sys.argv:
        print(Stats.get_csv_header())
    else:
        run_simulation()


def run_simulation():
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'config.txt'
    with open(filename, 'r') as file:
        CONFIG.parse(file)

    from simulation.event import ArrivalEndEvent

    SIMULATION.reset(lambda: ArrivalEndEvent(patient=SIMULATION.new_patient()))
    SIMULATION.run()
    # print('\n'.join(map(str, SIMULATION.event_log)))
    stats = Stats.calculate(SIMULATION)
    # print(stats)
    print(stats.get_csv())


if __name__ == '__main__':
    main()
