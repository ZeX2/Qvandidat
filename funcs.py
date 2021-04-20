from collections.abc import Iterable
import itertools
import time
import operator

import numpy as np
import scipy.optimize as opt

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
    
    for gamma_k, beta_k in zip(gamma, beta):
        if not gamma_k == 0:
            for i in range(N):
                for j in range(i):
                    if J[i,j] == 0: continue
                    qc.cx(i, j)
                    qc.rz(2*gamma_k*J[i,j], j)
                    qc.cx(i, j)
                    
            for i in range(N):
                if h[i] == 0: continue
                qc.rz(2*gamma_k*h[i], i)
        
        if beta_k == 0: continue
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

def expected_cost(J, h, const, TrJ, gamma, beta, costs, histogram=False,dict_ = False):
    qc = qaoa_ising_circuit(J, h, gamma, beta, measure=False)
    sv = execute(qc, SVSIM).result().get_statevector()
    sv = Statevector(sv)
    prob_dict = sv.probabilities_dict()
    cd = sorted(prob_dict.items(),key=operator.itemgetter(1),reverse=False)
    if dict_:    
        print(cd)
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

def _optimize_simulation(angles, *variables):
    J, h, const, TrJ, costs = variables
    gamma = angles[:len(angles)//2]
    beta = angles[len(angles)//2:]
    return expected_cost(J, h, const, TrJ, gamma, beta, costs)

def optimize_angles(p, J, h, const, TrJ, all_costs, iter_=1, out=False):
    bnd = opt.Bounds([0]*(2*p), [2*np.pi, np.pi]*p)
    t0 = time.time()
    angles = []
    costs = []
    args = (J, h, const, TrJ, all_costs)

    for i in range(iter_): 
        opt_angles = opt.differential_evolution(_optimize_simulation, bounds=bnd, args=args, disp=out)
        angles.append(opt_angles.x)
        costs.append(_optimize_simulation(opt_angles.x, *args))

    t1 = time.time()
    time_opt = t1-t0
    cost = min(costs)
    angles = angles[costs.index(costs)]
    angles = (angles[:len(angles)//2], angles[len(angles)//2:])
    print("Run time for optimization of angles was " + time.strftime("%H:%M:%S", time.gmtime(time_opt)))
    return angles, cost
