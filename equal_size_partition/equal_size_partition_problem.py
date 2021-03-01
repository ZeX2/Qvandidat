from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np
from qiskit import(
  QuantumCircuit,
  execute,
  Aer)

from get_ising_model import get_ising_model
from cost_function import cost_function

#S = np.array([4, 5, 13, 8, 3, 6, 3, 25, 4, 10, 8, 12, 8, 9, 7, 5, 6, 7, 10, 11, 4, 2, 5, 3, 10, 9, 12, 13])
#S = np.array([4, 5, 13, 8, 3, 6, 3, 25, 4, 10, 8, 12, 8, 9, 7, 5, 6, 7, 10, 11, 4, 2, 5, 3, 10, 10])
#S = np.array([2, 2, 1, 1])

S = np.array([2, 3, 3, 3, 3, 2, 1, 1])

beta = 1
gamma = np.pi/5

def expectation_value(S, beta, gamma, repetitions = 1000):
    N = len(S)

    (J,h) = get_ising_model(S)

    # Quantum Circuit
    qc = QuantumCircuit(N, N)
    qc.h(range(N))
    qc.barrier()

    for i in range(N):
        for j in range(i-1):
            qc.cx(i, j)
            qc.rz(2*gamma*J[i,j], j)
            qc.cx(i, j)

    qc.barrier()
    qc.rx(2*beta, range(N))

    # Simulate
    backend = Aer.get_backend('unitary_simulator')
    simulator = Aer.get_backend('qasm_simulator')

    qc.measure(range(N),range(N))
    job = execute(qc, simulator, shots=repetitions)
    result = job.result()

    counts = result.get_counts(qc)
    
    exp_val = 0
    best_sol = []
    best_sol_cost = -1

    print('%d states evaluated of %d total states' % (len(counts.keys()), 2**N))

    for bits in counts:
        value = counts[bits]
        
        spins = [1 if bit == '1' else -1 for bit in bits]

        cost = cost_function(spins, J)
        exp_val += value * cost / repetitions

        if best_sol_cost > cost or best_sol_cost == -1:
            best_sol_cost = cost
            best_sol = spins

    return (exp_val, best_sol)

def decode_state(state, S):
    (a, b) = ([], [])
    partition_difference = 0

    # It is probably possible to this in some nice pythonic way
    for si,s in enumerate(state):
        if s == 1: a.append(S[si])
        else: b.append(S[si])

    return (a, b)

(exp_val, state) = expectation_value(S, beta, gamma)
(a,b) = decode_state(state, S)

assert(sum(a) == sum(b))

print('Sums are equal with sum ', sum(a))
print(a, b)

