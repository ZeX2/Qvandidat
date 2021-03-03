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


def get_circuit(gammas, betas):
    if not isinstance(gammas, np.ndarray):
        gammas = np.array([gammas])
        betas = np.array([betas])

    p = len(gammas)

    (q1, q2) = (0, 1)

    circuit = QuantumCircuit(2, 2)
    circuit.h(q1)
    circuit.h(q2)

    for k in range(p):
        gamma = gammas[k]
        beta = betas[k]

        circuit.h(q2)
        circuit.rx(gamma, q2)
        circuit.cz(q1, q2)
        circuit.rz(gamma, q1)
        circuit.h(q2)
        circuit.rx(2*beta, q1)
        circuit.rx(2*beta, q2)

    circuit.measure([q1, q2], [0, 1])

    return circuit


def cost_function(x1, x2):
    j_12 = 1/2
    h_1 = 1/2
    s1 = 1 - 2*x1
    s2 = 1 - 2*x2

    return j_12*s1*s2 + h_1*s1 + 1


# cmd + shift + p -> Select Interpreter, pyton (noise)
