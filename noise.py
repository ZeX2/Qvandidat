import math
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise import pauli_error, depolarizing_error, amplitude_damping_error, phase_damping_error

def chalmers_probability_phase_damp(gate):
    T_1 = 55*10**(-6)
    T_22 = 49*10**(-6)
    T_2 = 1/((1/T_22)+(1/(2*T_1)))

    if gate == 1:
        t = 50*10**(-9)

    if gate == 2:
        t = 271*10**(-9)

    p = 0.5*(1 + math.exp(-t/T_2))

    # return 1-p

    gamma = 1 - (2*(1-p) - 1)**2

    return gamma


def chalmers_probability_amp_damp(gate):
    T_1 = 55*10**(-6)

    if gate == 1:
        t = 50*10**(-9)

    if gate == 2:
        t = 271*10**(-9)

    p = 1 - math.exp(-t/T_1)

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


