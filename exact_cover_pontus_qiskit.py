from qiskit.visualization import plot_histogram
from qiskit import(
    QuantumCircuit,
    execute,
    Aer)
import numpy as np
from exact_cover_pontus_cost_function import cost_function
from exact_cover_pontus_probability import calculate_probability
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise import pauli_error, depolarizing_error


simulator = Aer.get_backend('qasm_simulator')


def expectation_value(gamma, beta, repetitions=50):

    p1 = calculate_probability(0.99, 2)
    p2 = calculate_probability(0.99, 4)

    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.rx(gamma, 1)
    circuit.cz(0, 1)
    circuit.rz(gamma, 0)
    circuit.rx(2*beta, 0)
    circuit.h(1)
    circuit.rx(2*beta, 1)
    circuit.measure([0, 1], [0, 1])

    noise_model = NoiseModel()

    depo_error_1 = depolarizing_error(p1, 1)
    depo_error_2 = depolarizing_error(p2, 2)
    noise_model.add_all_qubit_quantum_error(depo_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(depo_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)
    job = execute(circuit, noisy_simulator, shots=repetitions)

    results = job.result()
    count_results = results.get_counts(0)

    C = 0
    for key in count_results:
        value = count_results
        C += value[key]*cost_function(int(key[0]), int(key[1]))

    return C/repetitions


# cmd + shift + p -> Select Interpreter, pyton (noise)
