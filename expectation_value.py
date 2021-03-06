from qiskit.visualization import plot_histogram
from qiskit import(
    QuantumCircuit,
    execute,
    Aer)
import numpy as np
from depolarizing_probability import depolarizing_probability
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise import pauli_error, depolarizing_error

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


def expectation_value(job, cost_function):

    results = job.result()
    count_results = results.get_counts()

    total_cost = 0
    total_counts = sum(count_results.values())
    cost_best = -1
    z_best = []

    for key in count_results:
        value = count_results[key]
        # Note: q1 is the leftmost bit

        spins = [1 if s == '1' else -1 for s in key]

        cost = cost_function(spins)
        total_cost += value*cost

        if cost < cost_best or cost_best == -1:
            cost_best = cost
            z_best = spins

    return (total_cost/total_counts, z_best)


def expectation_value_bitflip_job(fidelity, circuit, repetitions=50):
    p1 = depolarizing_probability(fidelity, 2)
    p2 = depolarizing_probability(fidelity, 4)

    noise_model = NoiseModel()

    depo_error_1 = pauli_error(p1, 1)
    depo_error_2 = pauli_error(p2, 2)
    noise_model.add_all_qubit_quantum_error(depo_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(depo_error_2, ['cz'])

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
