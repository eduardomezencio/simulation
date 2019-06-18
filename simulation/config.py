from typing import Dict, List, TextIO, Tuple

from simulation.distribution import Distribution, distribution_factory


class Config:

    t_tts: float  # Simulation time
    p_pro: float  # Need exams probablility
    p_pri: Tuple[float, float, float, float, float]  # Priority probability
    p_que: Tuple[float, float, float, float, float]  # Queue probability
    q_med: int  # Number of doctors
    q_enf: int  # Number of nurses
    q_atd: int  # Number of attendants
    t_che: Distribution  # Patient arrival time
    t_cad: Distribution  # Registering time
    t_tri: Distribution  # Screening time
    t_ate: Distribution  # Consultation time
    t_exa: Distribution  # Exams time

    def parse(self, file: TextIO):
        data: Dict[str, List[str]] = {}
        for line in file:
            line = line.split('#')[0].split()
            if len(line) >= 3:
                data['_'.join(s.lower() for s in line[:2])] = line[2:]
        for key in ('t_tts', 'p_pro'):
            self.__dict__[key] = float(data[key][0])
        for key in ('p_pri', 'p_que'):
            sum_pri = sum(float(s) for s in data[key])
            self.__dict__[key] = tuple(float(s) / sum_pri for s in data[key])
        for key in ('q_med', 'q_enf', 'q_atd'):
            self.__dict__[key] = int(data[key][0])
        for key in ('t_che', 't_cad', 't_tri', 't_ate', 't_exa'):
            self.__dict__[key] = distribution_factory(
                data[key][0], *(float(s) for s in data[key][1:4]))


INSTANCE = Config()
