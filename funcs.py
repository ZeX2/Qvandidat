from collections.abc import Iterable
import itertools

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import scipy.optimize as opt
import time
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
def optimize_simulation(angles,*variables):
    J, h, const, TrJ = variables
    if len(angles)==2:
        gamma,beta = angles
    elif len(angles)==4:
        gamma1,gamma2,beta1,beta2 = angles
        gamma = [gamma1,gamma2]
        beta = [beta1,beta2]
    elif len(angles)==6:
        gamma1,gamma2,gamma3,beta1,beta2,beta3 = angles
        gamma = [gamma1,gamma2,gamma3]
        beta = [beta1,beta2,beta3]
    elif len(angles)==8:
        gamma1,gamma2,gamma3,gamma4,beta1,beta2,beta3,beta4 = angles
        gamma = [gamma1,gamma2,gamma3,gamma4]
        beta = [beta1,beta2,beta3,beta4]
    elif len(angles)==10:
        gamma1,gamma2,gamma3,gamma4,gamma5,beta1,beta2,beta3,beta4,beta5 = angles
        gamma = [gamma1,gamma2,gamma3,gamma4,gamma5]
        beta = [beta1,beta2,beta3,beta4,beta5]
    elif len(angles)==12:
        gamma1,gamma2,gamma3,gamma4,gamma5,gamma6,beta1,beta2,beta3,beta4,beta5,beta6 = angles
        gamma = [gamma1,gamma2,gamma3,gamma4,gamma5,gamma6]
        beta = [beta1,beta2,beta3,beta4,beta5,beta6]
    return run_simulation(J,h,const,TrJ,gamma,beta,shots = 1000)
def optimize_angles(p,J,h,const,TrJ,iter_=1,out=False):
    
    bnd = opt.Bounds([0]*(2*p),[2*np.pi,np.pi]*p)
    t0 =time.time()
    list_angles=[]
    list_cost=[]
    args=(J,h,const,TrJ)
    for i in range(iter_): 
        opt_angles=opt.differential_evolution(optimize_simulation,bounds = bnd,args = args,disp = out)
        list_angles.append(opt_angles.x)
        print(opt_angles.x)
        list_cost.append(optimize_simulation(opt_angles.x,*args))
        print(optimize_simulation(opt_angles.x,*args))
        i+=1
    t1=time.time()
    time_opt = t1-t0
    cost = min(list_cost)
    angles = list_angles[list_cost.index(cost)]
    print("run time for optimization of angles was "+str(time_opt))
    return angles, cost