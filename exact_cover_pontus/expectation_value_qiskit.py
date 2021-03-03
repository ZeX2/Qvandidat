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


def expectation_value(gamma, beta, repetitions=50):

    p1 = depolarizing_probability(0.99, 2)
    p2 = depolarizing_probability(0.99, 4)

    (q1, q2) = (0, 1)

    circuit = QuantumCircuit(2, 2)

    noise_model = NoiseModel()

    depo_error_1 = depolarizing_error(p1, 1)
    depo_error_2 = depolarizing_error(p2, 2)
    noise_model.add_all_qubit_quantum_error(depo_error_1, ['h', 'rx', 'rz'])
    noise_model.add_all_qubit_quantum_error(depo_error_2, ['cz'])

    noisy_simulator = QasmSimulator(noise_model=noise_model)
    circuit.h(q1)
    circuit.rx(gamma, q2)
    circuit.cz(q1, q2)
    circuit.rz(gamma, q1)
    circuit.h(q2)
    circuit.rx(2*beta, q1)
    circuit.rx(2*beta, q2)
    circuit.measure([q1, q2], [0, 1])

    job = execute(circuit, noisy_simulator, shots=repetitions)

    results = job.result()
    count_results = results.get_counts()

    C = 0
    for key in count_results:
        value = count_results[key]
        # Note: q1 is the leftmost bit
        C += value*cost_function(int(key[1]), int(key[0]))

    return C/repetitions


def cost_function(x1, x2):
    j_12 = 1/2
    h_1 = 1/2
    s1 = 1 - 2*x1
    s2 = 1 - 2*x2

    return j_12*s1*s2 + h_1*s1 + 1


# cmd + shift + p -> Select Interpreter, pyton (noise)
