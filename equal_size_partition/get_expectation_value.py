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


def expectation_value(circuit, cost_function, repetitions=50, with_noise=True):

    if with_noise:
        job = measure_with_noise(circuit, repetitions)
    else:
        job = measure_without_noise(circuit, repetitions)

    results = job.result()
    count_results = results.get_counts()

    expval = 0
    cost = 0
    cost_best = -1
    z_best = []

    for key in count_results:
        value = count_results[key]
        # Note: q1 is the leftmost bit

        spins = [1 if s == '1' else -1 for s in key]

        cost = cost_function(spins)
        expval += value*cost/repetitions

        if cost < cost_best or cost_best == -1:
            cost_best = cost
            z_best = spins

    return expval, z_best

def expectation_value_job(job, cost_function):

    results = job.result()
    count_results = results.get_counts()

    expval = 0
    cost = 0
    cost_best = -1
    z_best = []

    for key in count_results:
        value = count_results[key]
        # Note: q1 is the leftmost bit

        spins = [1 if s == '1' else -1 for s in key]

        cost = cost_function(spins)
        expval += value*cost/repetitions

        if cost < cost_best or cost_best == -1:
            cost_best = cost
            z_best = spins

    return expval, z_best

def expectation_value_bitflip(probability, circuit, cost_function, repetitions=50):
    p1 = depolarizing_probability(probability, 2)
    p2 = depolarizing_probability(probability, 4)

    noise_model = NoiseModel()

    depo_error_1 = pauli_error(p1, 1)
    depo_error_2 = pauli_error(p2, 2)
    noise_model.add_all_qubit_quantum_error(depo_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(depo_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)

    job = execute(circuit, noisy_simulator, shots=repetitions)
    
    return expectation_value_job(job, cost_function)


def expectation_value_depolarizing(probability, circuit, cost_function, repetitions=50):
    p1 = depolarizing_probability(probability, 2)
    p2 = depolarizing_probability(probability, 4)

    noise_model = NoiseModel()

    depo_error_1 = depolarizing_error(p1, 1)
    depo_error_2 = depolarizing_error(p2, 2)
    noise_model.add_all_qubit_quantum_error(depo_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(depo_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)

    job = execute(circuit, noisy_simulator, shots=repetitions)
    
    return expectation_value_job(job, cost_function)


def measure_with_noise(circuit, repetitions):

    p1 = depolarizing_probability(0.99, 2)
    p2 = depolarizing_probability(0.99, 4)

    noise_model = NoiseModel()

    depo_error_1 = depolarizing_error(p1, 1)
    depo_error_2 = depolarizing_error(p2, 2)
    noise_model.add_all_qubit_quantum_error(depo_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(depo_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)

    job = execute(circuit, noisy_simulator, shots=repetitions)

    return job

def expectation_value_no_noise(circuit, cost_function, repetitions):
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=repetitions)

    return expectation_value_job(job, cost_function)


def measure_without_noise(circuit, repetitions):
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=repetitions)

    return job
# cmd + shift + p -> Select Interpreter, pyton (noise)
