from collections.abc import Iterable
import itertools
import time
import operator
import json
import ast
import os

import numpy as np
import scipy.optimize as opt

from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
#from qiskit_textbook.tools import array_to_latex
from integer_bin_packing import *

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

def expected_cost(J, h, const, TrJ, gamma, beta, costs, histogram=False, probs = False):
    qc = qaoa_ising_circuit(J, h, gamma, beta, measure=False)
    sv = execute(qc, SVSIM).result().get_statevector()
    sv = Statevector(sv)
    prob_dict = sv.probabilities_dict()
    sorted_probs = sorted(prob_dict.items(),key=operator.itemgetter(1),reverse=False)
    
    if probs:    
        print(sorted_probs)
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
    bnd = opt.Bounds([0]*(2*p), [2*np.pi]*p + [np.pi]*p)
    print(bnd)
    t0 = time.time()
    angles = []
    costs = []
    args = (J, h, const, TrJ, all_costs)

    for i in range(iter_): 
        opt_angles = opt.differential_evolution(_optimize_simulation, bounds=bnd, args=args, disp=out,maxiter = 8000)
        angles.append(opt_angles.x)
        costs.append(_optimize_simulation(opt_angles.x, *args))

    t1 = time.time()
    time_opt = t1-t0
    cost = min(costs)
    angles = angles[costs.index(costs)]
    angles = (angles[:len(angles)//2], angles[len(angles)//2:])
    print("Run time for optimization of angles was " + time.strftime("%H:%M:%S", time.gmtime(time_opt)))
    return angles, cost
def get_data_for_p(p,problem_instance,true_constant=False,path=False):
    search_string = "angles-p"+str(p)
    print(search_string)
    file_list = list()
    if not path:
        path = "C:\\Users\\Isak Brundin\\Downloads\\Qvandidat-data-analysis\\Qvandidat-data-analysis\\data"
    all_files = os.listdir(path)
    
    for file_name in all_files:
        if search_string in file_name and file_name.endswith('.json'):
            
            if "'W'_ [1]" in file_name and problem_instance == 1:
                file_list.append(os.path.join(path,file_name))
                print("h1j")
            elif "'W'_ [1, 1]" in file_name and problem_instance == 2:
                print("h2j")
                file_list.append(os.path.join(path,file_name))
            elif "'W'_ [1, 1, 1]" in file_name and problem_instance == 3:
                file_list.append(os.path.join(path,file_name))
            else:
                print("nej")
    if true_constant:
        true_constant_file_list = list()
        for file_ in file_list:    
            if true_constant == int(file_.split("'A'_ ")[1].split(", 'B'_ ")[0]):

                true_constant_file_list.append(file_)
   
        return true_constant_file_list
    return file_list
def data_extracter(json_file):
    with open(json_file) as f:
    
        data_dict = json.load(f)

    problem_dict = ast.literal_eval(data_dict["problem_identifier"])
    J,h,const,A,B,C = integer_bin_packing(problem_dict["W"],problem_dict["W_max"],problem_dict["A"],problem_dict["B"],problem_dict["C"])
    TrJ = np.trace(J)
    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, TrJ)/B for bits in bits_list}
    qc = qaoa_ising_circuit(J, h, data_dict["optimal_gammas"],data_dict["optimal_betas"], measure=False)
    sv = execute(qc, SVSIM).result().get_statevector()
    sv = Statevector(sv)
    prob_dict = sv.probabilities_dict()
    costs_freq = dict()
    for bits, prob in prob_dict.items():
        cost = costs[bits]
        if cost not in costs_freq:
            costs_freq[cost] = prob
        else:
            costs_freq[cost] += prob
    print(costs_freq)
    return costs_freq
def extracted_data_for_p(json_list):
    p1W11json =list()
    for i in range(len(json_list)):
        p1W11json.append(data_extracter(json_list[i]))
        i+=1
    return p1W11json
def best_optimal(costs_list,histogram = False,optimal_cost = 1.0):
    true_prob = 0
    true_prob_dict = {}
    
    for i in range(len(costs_list)):
        try:
            curr_prob = costs_list[i][optimal_cost]
        except:
            curr_prob = 0
        if curr_prob>true_prob:
            print(true_prob)
            true_prob = curr_prob
            true_prob_dict = costs_list[i]
    if histogram:
        plot_histogram(true_prob_dict)
    return true_prob_dict,true_prob

def avg_costs(costs_list,optimal_cost = 1.0):
    avg_dict = {}
    for i in range(len(costs_list)):
        for cost,prob in costs_list[i].items():
            if cost not in avg_dict:
                avg_dict[cost] = prob
            else:
                avg_dict[cost] += prob
    for cost,prob in avg_dict.items():
        avg_dict[cost] = avg_dict[cost]/float(len(costs_list))
    try:
        optimal_prob = avg_dict[optimal_cost]
    except:
        optimal_prob =0
    return avg_dict,optimal_prob
    
        
    