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

from native_gate_set import translate_circuit
from noise import chalmers_noise_model
from linear_swap import linear_swap_method as linear_swap

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
                    # linear_swap and swap_network requires rzz
                    qc.rzz(2*gamma_k*J[i,j], i, j) 
                    
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


def probability_cost_distribution_state(gamma, beta, J, h, costs):
    counts = _expected_cost(gamma, beta, J, h)
    return _probability_cost_distribution(counts, costs)

def probability_cost_distribution_simul(gamma, beta, J, h, costs, shots):
    prob_dict = _run_simulation(gamma, beta, J, h, shots)
    return _probability_cost_distribution(prob_dict, costs)

def _probability_cost_distribution(count_results, costs):
    total_counts = sum(count_results.values())
    total_cost = 0
    prob_dist = {}

    for key in count_results:
        value = count_results[key]

        cost = costs[key]
        prob_dist[cost] = prob_dist.get(cost, 0) + value/total_counts

    return prob_dist


def approximation_ratio_state(gamma, beta, J, h, costs):
    counts = _expected_cost(gamma, beta, J, h)
    return _approximation_ratio(counts, costs)

def approximation_ratio_simul(gamma, beta, J, h, costs, shots):
    prob_dict = _run_simulation(gamma, beta, J, h, shots)
    return _approximation_ratio(prob_dict, costs)

def _approximation_ratio(count_results, costs):

    total_cost = 0
    total_counts = sum(count_results.values())
    cost_best = None
    cost_max = -1

    for key in count_results:
        value = count_results[key]
        # Note: q1 is the leftmost bit

        spins = [1 if s == '1' else -1 for s in key]
        cost = costs[key]
        total_cost += value*cost
        
        if cost_best == None or cost < cost_best:
            cost_best = cost
        if cost > cost_max:
            cost_max = cost
    
    if cost_best == None:
        raise Exception('Invalid job, no costs found')

    exp_val = total_cost/total_counts
    return (exp_val - cost_max)/(cost_best - cost_max)


def _run_simulation(gamma, beta, J, h, shots):
    noise_model = chalmers_noise_model()
    chalmers_circuit = _chalmers_circuit(gamma, beta, J, h)
    job = execute(chalmers_circuit, SIMULATOR, shots=shots, noise_model=noise_model)
    result = job.result()
    return result.get_counts()

def run_simulation(gamma, beta, J, h, costs, shots):
    counts = _run_simulation(gamma, beta, J, h, shots)
    return sum(counts*costs[bits] for bits, counts in counts.items())/shots


# should produce the same results as expected_cost
def _run_chalmers_circuit_ideal(gamma, beta, J, h):
    circuit = _chalmers_circuit(gamma, beta, J, h)
    sv = execute(circuit, SVSIM).result().get_statevector()
    sv = Statevector(sv)
    return sv.probabilities_dict()

def run_chalmers_circuit_ideal(gamma, beta, J, h, costs):
    prob_dict = _run_chalmers_circuit_ideal(gamma, beta, J, h)
    return sum(prob*costs[bits] for bits, prob in prob_dict.items())


def _chalmers_circuit(gamma, beta, J, h):
    p = len(gamma) if isinstance(gamma, Iterable) else 1
    qaoa_circuit = qaoa_ising_circuit(J, h, gamma, beta)
    chalmers_coupling_circuit = linear_swap(qaoa_circuit, p)
    chalmers_circuit = translate_circuit(chalmers_coupling_circuit)
    return chalmers_circuit


def _expected_cost(gamma, beta, J, h):
    circuit = qaoa_ising_circuit(J, h, gamma, beta, measure=False)
    sv = execute(circuit, SVSIM).result().get_statevector()
    sv = Statevector(sv)
    return sv.probabilities_dict()

def expected_cost(gamma, beta, J, h, costs):
    prob_dict = _expected_cost(gamma, beta, J, h)
    return sum(prob*costs[bits] for bits, prob in prob_dict.items())


def _objective_state(angles,*variables):
    
    J, h, costs = variables
    gamma, beta = angles[:len(angles)//2], angles[len(angles)//2:]
    return expected_cost(gamma, beta, J, h, costs)

def optimize_angles_state(J, h, p, costs, maxiter):
    
    bnd = opt.Bounds([0]*(2*p), [2*np.pi]*p + [np.pi]*p) 
    args = (J, h, costs)
    opt_angles = opt.differential_evolution(_objective_state, bounds=bnd, args = args, maxiter = maxiter)
    angles = opt_angles.x

    return angles[:len(angles)//2], angles[len(angles)//2:], opt_angles

def _objective_simul(angles,*variables):
    J, h, costs, shots = variables
    gamma, beta = angles[:len(angles)//2], angles[len(angles)//2:]
    return run_simulation(gamma, beta, J, h, costs,shots)  

def optimize_angles_simul(J, h, p, costs, maxiter, shots = 1000):
    
    bnd = opt.Bounds([0]*(2*p), [2*np.pi]*p + [np.pi]*p)   
    args = (J,h,costs,shots)
    opt_angles = opt.differential_evolution(_objective_simul, bounds=bnd, maxiter = maxiter, args = args)
    angles = opt_angles.x

    return angles[:len(angles)//2], angles[len(angles)//2:], opt_angles

def landscape_state(J, h,costs,iter_):
    
    betas = np.linspace(0, np.pi, int(np.sqrt(iter_)))
    gammas = np.linspace(0, 2*np.pi, int(np.sqrt(iter_)))
    
    exp_costs = np.zeros((len(gammas), len(betas)))

    for i, beta in enumerate(betas):
        for j, gamma in enumerate(gammas):
            exp_costs[i,j] = expected_cost(gamma, beta, J, h, costs)
    
    return gammas, betas, exp_costs

def landscape_simul(J, h,costs,iter_,shots = 1000):
    
    betas = np.linspace(0, np.pi, int(np.sqrt(iter_)))
    gammas = np.linspace(0, 2*np.pi, int(np.sqrt(iter_)))
    
    exp_costs = np.zeros((len(gammas), len(betas)))

    for i, beta in enumerate(betas):
        for j, gamma in enumerate(gammas):
            exp_costs[i,j] = run_simulation(gamma, beta, J, h, costs,shots)
    
    return gammas, betas, exp_costs


