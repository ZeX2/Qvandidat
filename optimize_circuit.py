import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager, passes, CouplingMap, Layout
from qiskit.transpiler.passes import( 
    TrivialLayout,
    DenseLayout)
from qiskit.visualization import plot_circuit_layout

def simplify(circuit):
    return transpile(circuit, optimization_level=3)

def optimize_mapping(circuit, coupling, n):
    return transpile(circuit, coupling_map = coupling, optimization_level=n)

def optimize_circ(circuit, coupling_map, n):
    if n == 0:
        tl = TrivialLayout(coupling_map=coupling_map)
        pass_manager = PassManager(tl)
        return pass_manager.run(circuit)

    elif n == 1:
        dl = DenseLayout(coupling_map=coupling_map)
        pass_manager = PassManager(dl)
        return pass_manager.run(circuit)
