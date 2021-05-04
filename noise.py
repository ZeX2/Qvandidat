import math
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise import pauli_error, depolarizing_error, amplitude_damping_error, phase_damping_error

def chalmers_probability_phase_damp(gate):

    if gate == 1:
        T_2star = 49*10**(-6)
        t = 50*10**(-9)

    if gate == 2:
        T_2star = 82*10**(-6)
        t = 271*10**(-9)

    gamma = 1 - math.exp(-2*t/T_2star)

    return gamma


def chalmers_probability_amp_damp(gate):

    if gate == 1:
        T_1 = 77*10**(-6)
        t = 50*10**(-9)

    if gate == 2:
        T_1 = 55*10**(-6)
        t = 271*10**(-9)

    p = 1 - math.exp(-2*t/T_1)

    return p

def chalmers_noise_model():
    noise_model = NoiseModel()

    gamma1 = chalmers_probability_phase_damp(1)
    gamma2 = chalmers_probability_phase_damp(2)

    phasedamp_error_1 = phase_damping_error(gamma1)
    phasedamp_error_2 = phase_damping_error(gamma2)
    phasedamp_error_2 = phasedamp_error_2.tensor(phasedamp_error_2)

    p1 = chalmers_probability_amp_damp(1)
    p2 = chalmers_probability_amp_damp(2)

    ampdamp_error_1 = amplitude_damping_error(p1, 0)
    ampdamp_error_2 = amplitude_damping_error(p2, 0)
    ampdamp_error_2 = ampdamp_error_2.tensor(ampdamp_error_2)

    error_1 = phasedamp_error_1.compose(ampdamp_error_1)
    error_2 = phasedamp_error_2.compose(ampdamp_error_2)

    noise_model.add_all_qubit_quantum_error(error_1, ['rz', 'ry'])
    noise_model.add_all_qubit_quantum_error(error_2, ['cz', 'iswap', ''])

    return noise_model


