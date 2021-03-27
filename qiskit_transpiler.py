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

def swap_update(circuit, coupling, int):
    if (int != 0 and int != 1 and int != 2):
        return print('SWAP performance not defined')
    coupling_map = CouplingMap(couplinglist=coupling)
    if int == 0:
        bs = BasicSwap(coupling_map=coupling_map)
        pass_manager = PassManager(bs)
        basic_circ = pass_manager.run(circuit)
        basic_circ.draw(output='mpl', filename='Basic Swap')
        print('Basic Swap circuit depth', basic_circ.depth())
        return basic_circ
    elif int == 1:
        ls = LookaheadSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ls)
        lookahead_circ = pass_manager.run(circuit)
        lookahead_circ.draw(output='mpl', filename='Lookahead Swap')
        print('Lookahead Swap circuit depth', lookahead_circ.depth())
        return lookahead_circ
    elif int == 2:
        ss = StochasticSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ss)
        stochastic_circ = pass_manager.run(circuit)
        stochastic_circ.draw(output='mpl', filename='Stochastic Swap')
        print('Stochastic Swap circuit depth', stochastic_circ.depth())
        return stochastic_circ

def optimize_mapping(circuit, coupling, int):
    if (int != 1 and int != 2):
        return print('Gate mapping performance not defined')
    coupling_map = CouplingMap(couplinglist=coupling)
    if int == 1:
        tl = TrivialLayout(coupling_map=coupling_map)
        pass_manager = PassManager(tl)
        trivial_circ = pass_manager.run(circuit)
        return trivial_circ
    elif int == 2:
        dl = DenseLayout(coupling_map=coupling_map)
        pass_manager = PassManager(dl)
        dense_circ = pass_manager.run(circuit)
        return dense_circ