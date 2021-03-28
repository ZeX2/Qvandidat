import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager, passes, CouplingMap, Layout
from qiskit.transpiler.passes import(
    Unroller, 
    BasicSwap, 
    LookaheadSwap, 
    StochasticSwap, 
    TrivialLayout,
    DenseLayout,
    NoiseAdaptiveLayout) 
from swap_network import *
from qiskit_transpiler import *

def compare_circuit_depth(J, gamma, beta, coupling):
    N = len(J)
    qc = QuantumCircuit(N, N)
    qc.h(range(N))
    qc.barrier()
    
    for i in range(N):
        for j in range(i):
            qc.cx(i, j)
            qc.rz(2*gamma*J[i,j], j)
            qc.cx(i, j)
    
    qc.barrier()
    qc.rx(2*beta, range(N))
    qqc = qc.copy()

    for i in range(3):
        swap_update(qc, coupling, i)

    qc_swap_network = swap_network(qqc)
    qc_swap_network.draw(output='mpl', filename='SWAP network')

    print(qc_swap_network.depth())
    

