import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager, passes, CouplingMap, Layout
from qiskit.transpiler.passes import( 
    TrivialLayout,
    DenseLayout)
from qiskit.visualization import plot_circuit_layout



def optimize_mapping(circuit, backend, n):
    print(circuit)
    optimized_circ = transpile(circuit, backend = backend, optimization_level=n)
    print(optimized_circ)
    plot_circuit_layout(optimized_circ, backend)

def optimize_circuit(circuit, backend, coupling_map, n):
    if (n != 0 and n != 1):
        return print('Gate mapping performance not defined')

    if type(coupling_map) is not CouplingMap:
        coupling_map = CouplingMap(couplinglist=coupling_map)

    if n == 0:
        tl = TrivialLayout(coupling_map=coupling_map)
        pass_manager = PassManager(tl)
        trivial_circ = pass_manager.run(circuit)
        return trivial_circ
    elif n == 1:
        dl = DenseLayout(coupling_map=coupling_map)
        pass_manager = PassManager(dl)
        dense_circ = pass_manager.run(circuit)
        return dense_circ