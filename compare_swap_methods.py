import numpy as np
import math 
from swap_network import swap_network, get_qubit_grid
from qiskit_transpiler import swap_update
from equal_size_partition.gen_equal_size_partition_data import decode_file
from equal_size_partition.decode_state import decode_state
from equal_size_partition.get_circuit import get_circuit
from equal_size_partition.get_ising_model import get_ising_model
from qiskit.transpiler import CouplingMap
from qiskit.providers.aer import QasmSimulator
from qiskit import QuantumCircuit, execute
from linear_swap import linear_swap_method as linear
from optimize_circuit import *
from native_gate_set import translate_circuit
from five_qubit_swap_technique import star_swap
from linear_swap_grid import linear_swap_method


def run_circuit(circuit):
    ideal_simulator = QasmSimulator()

    # Execute and get counts
    result = execute(circuit, ideal_simulator, shots=100000).result()
    return result.get_counts(circuit)


decoded_file = decode_file('example_data_q4_q20')

for i, (arr, sol) in enumerate(decoded_file):

    if len(arr) != 16: continue
    
    if len(arr) not in [2**k for k in range(10)]:
        print('PASS')
        continue # only 2**k numbers of qubits allowed
         #4, 8, 16 out of q4_to_q20

    arr = [1,1,1]
    S = np.array(arr)
    gamma = np.array([np.random.rand() * np.pi,np.random.rand() * np.pi])
    beta = np.array([np.random.rand() * np.pi,np.random.rand() * np.pi])
    p = len(gamma)

    J, h, bounds = get_ising_model(S)
    qaoa_circuit = get_circuit(gamma, beta, J, h)

    # e.g. coupling = [[0,1], [0,2], [1,2]]

    qubit_grid = get_qubit_grid(2**math.ceil(math.log2(len(arr))))

    coupling = CouplingMap()
    rows, cols = qubit_grid.shape
    grid_coupling = coupling.from_grid(rows, cols)
    
    #grid_coupling = [[0,4], [4,0], [1,4], [4,1], [2,4], [4,2], [3,4], [4,3]]


    linear_swap_circuit = linear_swap_method(qaoa_circuit, p)
    #swap_network_circuit = swap_network(qaoa_circuit, p, qubit_grid)
    #trans = translate_circuit(swap_network_circuit)
    #print('yo',swap_update(trans, grid_coupling,4).count_ops())
    #print(trans)
    #basic_swap_circuit = swap_update(qaoa_circuit, grid_coupling, 0)
    #lookahead_swap_circuit = swap_update(qaoa_circuit, grid_coupling, 1)
    #stochastic_swap_circuit = swap_update(qaoa_circuit, grid_coupling, 2)
    #sabre_swap_circuit = swap_update(qaoa_circuit, grid_coupling, 3) # Why is this not working???
    #transpile_circuit = swap_update(qaoa_circuit, grid_coupling, 4)
    #transpile_circuit = swap_update(swap_network_circuit, grid_coupling, 4)
    #exit(0)
    linear_connectivity_circuit = linear(qaoa_circuit, p)
    #star_circuit = star_swap(qaoa_circuit, p)


    sim_ref = run_circuit(qaoa_circuit)
    #sim_swap = run_circuit(swap_network_circuit)
    #sim_basic = run_circuit(basic_swap_circuit)
    #sim_look = run_circuit(lookahead_swap_circuit)
    #sim_stoch = run_circuit(stochastic_swap_circuit)
    #sim_sabre = run_circuit(sabre_swap_circuit)
    #sim_linear = run_circuit(linear_connectivity_circuit)
    #sim_trans = run_circuit(transpile_circuit)
    #sim_star = run_circuit(star_circuit)
    sim_linear_swap = run_circuit(linear_swap_circuit)
    results = [];
    #for (key, val) in sim_ref.items():
        
    #    arr = np.array([sim_swap.get(key, 0), sim_basic.get(key, 0),\
    #            sim_look.get(key, 0), sim_stoch.get(key, 0), sim_sabre.get(key, 0)])
    #    results.append(arr - val)

    #results = np.asarray(results)
    #print([np.sum(np.abs(results),axis=0)])

    for (key, val) in sim_ref.items():
    
        print("{: <10} {: <10} {: <10}".format(val, sim_linear_swap.get(key, 0),\
            int(abs(sim_linear_swap.get(key, 0)-val) * 100 / val)))

    #print(qaoa_circuit)
    print(qaoa_circuit)

    print(linear_swap_circuit)
    print('qaoa depth', qaoa_circuit.depth())
    print('linear depth', linear_swap_circuit.depth())
    #print(swap_network_circuit)
    #print('swap depth', swap_network_circuit.depth())
    #print(translate_circuit(swap_network_circuit))
    #print('translated depth', translate_circuit(swap_network_circuit).depth())
    #print(transpile_circuit)
    #print('transpiled depth', transpile_circuit.depth())
    #print(translate_circuit(transpile_circuit))
    #print('translated transpile depth',translate_circuit(transpile_circuit).depth())
    #opt = simplify(swap_network_circuit)
    #print('Opt depth', opt.depth())
    #translated = translate_circuit(swap_network_circuit)
    #print(translated)
    #print('swap gates', translate_circuit(swap_network_circuit).count_ops())
    #print( 'transpiled gates', transpile_circuit.count_ops())
    #print('translated transpile gates', translate_circuit(transpile_circuit).count_ops())
    


    #print('trans',translated.depth())
    #opt = simplify(translated)
    #print(opt)
    #print('Opt depth', opt.depth())

    #print(basic_swap_circuit)
    #print(lookahead_swap_circuit)
    #print(stochastic_swap_circuit)
    #print(sabre_swap_circuit)
    #print(linear_connectivity_circuit)
    #print('linear swap new', linear_connectivity_circuit.depth())
    #print(star_circuit)

    #print('swap network %d, basic swap %d, lookahead swap %d, stochastic swap %d, sabre swap %d, linear swap %d' % \
        #(swap_network_circuit.depth(), basic_swap_circuit.depth(), lookahead_swap_circuit.depth(), \
         #stochastic_swap_circuit.depth(), sabre_swap_circuit.depth(), linear_connectivity_circuit.depth()))
    input()