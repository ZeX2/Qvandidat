import numpy as np
import math
import os
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager, passes, CouplingMap, Layout
from qiskit.transpiler.passes import(
    BasicSwap, 
    LookaheadSwap, 
    StochasticSwap, 
    SabreSwap,
    DenseLayout, NoiseAdaptiveLayout, SabreLayout) 
from .chalmers_backend import FakeChalmers

def swap_update(circuit, coupling_map, n, print_depth=True):
    if n not in range(0, 5):
        return print('SWAP performance not defined')
    
    if type(coupling_map) is not CouplingMap:
        coupling_map = CouplingMap(couplinglist=coupling_map)

    if print_depth: 
        os.makedirs('output', exist_ok=True) 

    if n == 0:
        bs = BasicSwap(coupling_map=coupling_map)
        pass_manager = PassManager(bs)
        basic_circ = pass_manager.run(circuit)
        if print_depth: 
            basic_circ.draw(output='mpl', filename='output/BasicSwap')
            print('Basic Swap circuit depth', basic_circ.depth())
        return basic_circ
    elif n == 1:
        ls = LookaheadSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ls)
        lookahead_circ = pass_manager.run(circuit)
        if print_depth: 
            lookahead_circ.draw(output='mpl', filename='output/LookaheadSwap')
            print('Lookahead Swap circuit depth', lookahead_circ.depth())
        return lookahead_circ
    elif n == 2:
        ss = StochasticSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ss)
        stochastic_circ = pass_manager.run(circuit)
        if print_depth: 
            stochastic_circ.draw(output='mpl', filename='output/StochasticSwap')
            print('Stochastic Swap circuit depth', stochastic_circ.depth())
        return stochastic_circ
    elif n == 3:
        ss = SabreSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ss)
        sabre_circ = pass_manager.run(circuit)
        if print_depth: 
            sabre_circ.draw(output='mpl', filename='output/SabreSwap')
            print('Sabre Swap circuit depth', sabre_circ.depth())
        return sabre_circ
    elif n == 4:
        backend = FakeChalmers()
        best_circuit = None
        for kk in range(4):
            circ = transpile(circuit, backend,  optimization_level=kk)
            #print(kk, circ.depth())
            if (best_circuit is None) or (best_circuit.depth() > circ.depth()):
                best_circuit = circ
                #print('vest', best_circuit.depth())
        return best_circuit

def transpile_circuit(circuit, print_depth=True):
    backend = FakeChalmers()
    best_circuit = None
    for kk in range(4):
        try:
            circ = transpile(circuit, backend,  optimization_level=kk)
        except ex:
            print('Transpiled failed with message', ex)
            try:
                circ = transpile(circuit, backend,  optimization_level=kk)
            except ex:
                print('Transpiled failed AGAIN now with message', ex)
                print('Ignoring this optimization_level', kk)
                continue

        if (best_circuit is None) or (best_circuit.depth() > circ.depth()):
            best_circuit = circ

    return best_circuit
