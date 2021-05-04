import math


def get_probability_phase_damp(gate):

    if gate == 1:
        T_2star = 49*10**(-6)
        t = 50*10**(-9)

    if gate == 2:
        T_2star = 82*10**(-6)
        t = 271*10**(-9)

    gamma = 1 - math.exp(-2*t/T_2star)

    return gamma


def get_probability_amp_damp(gate):

    if gate == 1:
        T_1 = 77*10**(-6)
        t = 50*10**(-9)

    if gate == 2:
        T_1 = 55*10**(-6)
        t = 271*10**(-9)

    p = 1 - math.exp(-2*t/T_1)

    return p


def depolarizing_probability(fidelity, d=2):
    return 3/4*(1 - (fidelity - 1/d)/(1 - 1/d))


#print('Probability of phase damp, 1 qubit gate: ', get_probability_phase_damp(1))
#print('Probability of phase damp, 2 qubit gate: ', get_probability_phase_damp(2))
#print('Probability of amplitude damp, 1 qubit gate: ', get_probability_amp_damp(1))
#print('Probability of amplitude damp, 2 qubit gate: ', get_probability_amp_damp(2))
