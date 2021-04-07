from qiskit.visualization import plot_histogram
from qiskit import(
    QuantumCircuit,
    execute,
    Aer)
import numpy as np
from depolarizing_probability import depolarizing_probability
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise import pauli_error, depolarizing_error, amplitude_damping_error, phase_damping_error
from get_probability import get_probability_amp_damp, get_probability_phase_damp, depolarizing_probability


def probability_cost_distribution(job, cost_function):

    results = job.result()
    count_results = results.get_counts()

    total_counts = sum(count_results.values())
    total_cost = 0
    prob_dist = {}

    for key in count_results:
        value = count_results[key]
        # Note: q1 is the leftmost bit
        spins = [1 if s == '1' else -1 for s in key]

        cost = cost_function(spins)
        total_cost += value*cost

        prob_dist[cost] = prob_dist.get(cost, 0) + value/total_counts

    return (prob_dist, total_cost/total_counts)


def approximation_ratio(expectation_value, cost_best, cost_max):

    r = (cost_best + cost_max)/(expectation_value + cost_max)

    return r


def expectation_value(job, cost_function):

    results = job.result()
    count_results = results.get_counts()

    total_cost = 0
    total_counts = sum(count_results.values())
    cost_best = 1000000000000
    cost_max = -1
    z_best = []

    for key in count_results:
        value = count_results[key]
        # Note: q1 is the leftmost bit

        spins = [1 if s == '1' else -1 for s in key]

        cost = cost_function(spins)
        total_cost += value*cost

        if cost < cost_best:
            cost_best = cost
            z_best = spins
        if cost > cost_max:
            cost_max = cost

    return (total_cost/total_counts, cost_best, cost_max)


def expectation_value_bitflip_job(fidelity, circuit, repetitions=50):
    p1 = depolarizing_probability(fidelity, 2)
    p2 = depolarizing_probability(fidelity, 4)

    noise_model = NoiseModel()

    bitflip_error_1 = pauli_error([('X', p1), ('I', 1 - p1)])
    bitflip_error_2 = bitflip_error_1.tensor(bitflip_error_1)

    noise_model.add_all_qubit_quantum_error(bitflip_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(bitflip_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)

    job = execute(circuit, noisy_simulator, shots=repetitions)

    return job


def expectation_value_phaseflip_job(fidelity, circuit, repetitions=50):
    p1 = depolarizing_probability(fidelity, 2)
    p2 = depolarizing_probability(fidelity, 4)

    noise_model = NoiseModel()

    phaseflip_error_1 = pauli_error([('Z', p1), ('I', 1 - p1)])
    phaseflip_error_2 = phaseflip_error_1.tensor(phaseflip_error_1)

    noise_model.add_all_qubit_quantum_error(
        phaseflip_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(phaseflip_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)

    job = execute(circuit, noisy_simulator, shots=repetitions)

    return job


def expectation_value_ampdamp_job(fidelity, circuit, repetitions=50):
    #p1 = depolarizing_probability(fidelity, 2)
    #p2 = depolarizing_probability(fidelity, 4)

    noise_model = NoiseModel()

    p1 = get_probability_amp_damp(1)
    p2 = get_probability_amp_damp(2)

    ampdamp_error_1 = amplitude_damping_error(p1, 0)

    ampdamp_error_2 = amplitude_damping_error(p2, 0)
    ampdamp_error_2 = ampdamp_error_2.tensor(ampdamp_error_2)

    noise_model.add_all_qubit_quantum_error(ampdamp_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(ampdamp_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)

    job = execute(circuit, noisy_simulator, shots=repetitions)

    return job


def expectation_value_phasedamp_job(fidelity, circuit, repetitions=50):
    #p1 = depolarizing_probability(fidelity, 2)
    #p2 = depolarizing_probability(fidelity, 4)

    #gamma = 1 - (2*p1 - 1)**2
    #gamma2 = 1 - (2*p2 - 1)**2

    gamma1 = get_probability_phase_damp(1)
    gamma2 = get_probability_phase_damp(2)

    noise_model = NoiseModel()

    phasedamp_error_1 = phase_damping_error(gamma1)

    phasedamp_error_2 = phase_damping_error(gamma2)
    phasedamp_error_2 = phasedamp_error_2.tensor(phasedamp_error_2)

    noise_model.add_all_qubit_quantum_error(
        phasedamp_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(phasedamp_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)

    job = execute(circuit, noisy_simulator, shots=repetitions)

    return job


def expectation_value_amp_phase_damp_job(circuit, repetitions=50):
    #p1 = depolarizing_probability(fidelity, 2)
    #p2 = depolarizing_probability(fidelity, 4)

    noise_model = NoiseModel()

    gamma1 = get_probability_phase_damp(1)
    gamma2 = get_probability_phase_damp(2)

    phasedamp_error_1 = phase_damping_error(gamma1)
    phasedamp_error_2 = phase_damping_error(gamma2)
    phasedamp_error_2 = phasedamp_error_2.tensor(phasedamp_error_2)

    p1 = get_probability_amp_damp(1)
    p2 = get_probability_amp_damp(2)

    ampdamp_error_1 = amplitude_damping_error(p1, 0)
    ampdamp_error_2 = amplitude_damping_error(p2, 0)
    ampdamp_error_2 = ampdamp_error_2.tensor(ampdamp_error_2)

    error_1 = phasedamp_error_1.compose(ampdamp_error_1)
    error_2 = phasedamp_error_2.compose(ampdamp_error_2)

    noise_model.add_all_qubit_quantum_error(error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)

    job = execute(circuit, noisy_simulator, shots=repetitions)

    return job


def expectation_value_depolarizing_job(fidelity, circuit, repetitions=50):
    p1 = depolarizing_probability(fidelity, 2)
    p2 = depolarizing_probability(fidelity, 4)
    noise_model = NoiseModel()

    depo_error_1 = depolarizing_error(p1, 1)
    depo_error_2 = depolarizing_error(p2, 2)
    noise_model.add_all_qubit_quantum_error(depo_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(depo_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)

    job = execute(circuit, noisy_simulator, shots=repetitions)

    return job


def expectation_value_no_noise_job(circuit, repetitions=50):
    simulator = QasmSimulator()
    #simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=repetitions)

    return job

# cmd + shift + p -> Select Interpreter, pyton (noise)
