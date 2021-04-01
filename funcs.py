from collections.abc import Iterable
import itertools

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
#%matplotlib agg

from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
#from qiskit_textbook.tools import array_to_latex

BACKEND = Aer.get_backend('unitary_simulator')
SIMULATOR = Aer.get_backend('qasm_simulator')
SVSIM = Aer.get_backend('statevector_simulator')

def qaoa_ising_circuit(J, h, gamma, beta, draw_circuit=False, measure=True):
    if not (isinstance(gamma, Iterable) and isinstance(beta, Iterable)):
        gamma = [gamma]
        beta = [beta]

    N = len(J)
    qc = QuantumCircuit(N, N)
    qc.h(range(N))
    #qc.barrier()
    
    for gamma_k, beta_k in zip(gamma, beta):
        for i in range(N):
            for j in range(i):
                qc.cx(i, j)
                qc.rz(2*gamma_k*J[i,j], j)
                qc.cx(i, j)
                
        for i in range(N):
            qc.rz(2*gamma_k*h[i], i)
        
        #qc.barrier()
        qc.rx(2*beta_k, range(N))

    if measure:
        qc.measure_all()
    if draw_circuit:
        qc.draw(output='mpl', filename='circuit')
    return qc

def bits_to_spins(bits):
    if isinstance(bits, str):
        return [1 if bit == '1' else -1 for bit in bits]
    else:
        return [1 if bit == 1 else -1 for bit in bits]

def get_bits_list(n):
    return [''.join(i) for i in itertools.product('01', repeat=n)]

def cost_function(bits, J, h, const, TrJ=None):
    if not TrJ:
        TrJ = np.trace(J)
    N = len(J)
    spins = bits_to_spins(bits)
    cost = TrJ + const
    cost += 2*sum((J[i,j]*spins[i]*spins[j] for i in range(N) for j in range(i)))
    cost += sum(h[i]*spins[i] for i in range(N))
    
    return cost

def run_simulation(J, h, const, TrJ, gamma, beta, shots=1000, draw_circuit=False, histogram=False):
    qc = qaoa_ising_circuit(J, h, gamma, beta, draw_circuit)
    job = execute(qc, SIMULATOR, shots=shots)
    result = job.result()
    counts = result.get_counts(qc)

    costs = dict()
    for bits, count in counts.items():
        cost = cost_function(bits, J, h, const, TrJ)
        if cost not in costs:
            costs[cost] = count
        else:
            costs[cost] += count
    
    if histogram: 
        plot_histogram(costs)

    avg_cost = sum(count*cost for cost, count in costs.items())/shots
    return avg_cost

# Remove const and TrJ as input variables, not used
def expected_cost(J, h, const, TrJ, gamma, beta, costs, histogram=False):
    qc = qaoa_ising_circuit(J, h, gamma, beta, measure=False)
    job = execute(qc, SVSIM)
    sv = job.result().get_statevector()
    sv = Statevector(sv)
    prob_dict = sv.probabilities_dict()

    if histogram:
        costs_freq = dict()
        for bits, prob in prob_dict.items():
            cost = costs[bits]
            if cost not in costs_freq:
                costs_freq[cost] = prob
            else:
                costs_freq[cost] += prob
    
        plot_histogram(costs_freq)

    return sum(prob*costs[bits] for bits, prob in prob_dict.items())
