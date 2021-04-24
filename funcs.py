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

def qaoa_ising_circuit(J, h, gamma, beta, measure=True):
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


def run_simulation(gamma, beta, J, h, costs, shots):
    #TODO add noice
    circuit = qaoa_ising_circuit(J, h, gamma, beta)
    job = execute(circuit, SIMULATOR, shots=shots)
    result = job.result()
    counts = result.get_counts()

    return sum(counts*costs[bits] for bits, counts in counts.items())/shots

def expected_cost(gamma, beta, J, h, costs):
    circuit = qaoa_ising_circuit(J, h, gamma, beta)
    sv = execute(circuit, SVSIM).result().get_statevector()
    sv = Statevector(sv)
    prob_dict = sv.probabilities_dict()

    return sum(prob*costs[bits] for bits, prob in prob_dict.items())

def optimize_angles_state(J, h, p, costs, maxiter):
    bnd = opt.Bounds([0]*(2*p), [np.pi]*p + [np.pi/2]*p)
    
    def objective(angles):
        gamma, beta = angles[:len(angles)//2], angles[len(angles)//2:]
        return expected_cost(gamma, beta, J, h, costs)
 
    opt_angles = opt.differential_evolution(objective, bounds=bnd, maxiter = maxiter)
    angles = opt_angles.x

    return angles[:len(angles)//2], angles[len(angles)//2:]
   
def optimize_angles_simul(J, h, p, costs, maxiter, shots = 1000):
    bnd = opt.Bounds([0]*(2*p), [np.pi]*p + [np.pi/2]*p)
    
    def objective(angles):
        gamma, beta = angles[:len(angles)//2], angles[len(angles)//2:]
        return run_simulation(gamma, beta, J, h, costs,shots)
 
    opt_angles = opt.differential_evolution(objective, bounds=bnd, maxiter = maxiter)
    angles = opt_angles.x

    return angles[:len(angles)//2], angles[len(angles)//2:]

def landscape_state(J, h,costs,iter_,step_size):
    
    betas = np.linspace(0, np.pi, int(np.sqrt(iter_)))
    gammas = np.linspace(0, 2*np.pi, int(np.sqrt(iter_)))
    
    exp_costs = np.zeros((len(gammas), len(betas)))

    for i, beta in enumerate(betas):
        for j, gamma in enumerate(gammas):
            exp_costs[i,j] = expected_cost(gamma, beta, J, h, costs)
    
    return exp_costs

def landscape_simul(J, h,costs,iter_,step_size,shots = 1000):
    
    betas = np.linspace(0, np.pi, int(np.sqrt(iter_)))
    gammas = np.linspace(0, 2*np.pi, int(np.sqrt(iter_)))
    
    exp_costs = np.zeros((len(gammas), len(betas)))

    for i, beta in enumerate(betas):
        for j, gamma in enumerate(gammas):
            exp_costs[i,j] = run_simulation(gamma, beta, J, h, costs,shots)
    
    return gammas, betas, exp_costs