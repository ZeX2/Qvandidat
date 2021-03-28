import math


def get_probability_phase_damp(gate):
    T_1 = 77*10**(-6)
    T_22 = 49*10**(-6)
    T_2 = 1/((1/T_22)+(1/2*T_1))

    if gate == 1:
        t = 50*10**(-9)

    if gate == 2:
        t = 271*10**(-9)

    p = 0.5*(1 + math.exp(-T_2*t))
    gamma = 1 - (2*(1-p) - 1)**2

    return gamma


def get_probability_amp_damp(gate):
    T_1 = 77*10**(-6)

    if gate == 1:
        t = 50*10**(-9)

    if gate == 2:
        t = 271*10**(-9)

    p = 1 - math.exp(-t/T_1)

    return p
