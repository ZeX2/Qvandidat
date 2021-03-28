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

def change_bases(circuit, bases):
    pass_ = Unroller(bases)
    pm = PassManager(pass_)
    new_circuit = pm.run(circuit)
    return new_circuit

def rotatex(qubit, angle):
    qubit.ry(np.pi/2)
    qubit.rz(angle)
    qubit.ry(np.pi/2)
    return qubit