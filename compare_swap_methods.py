import numpy as np
from swap_network import swap_network, get_qubit_grid
from qiskit_transpiler import swap_update
from equal_size_partition.gen_equal_size_partition_data import decode_file
from equal_size_partition.decode_state import decode_state
from equal_size_partition.get_circuit import get_circuit
from equal_size_partition.get_ising_model import get_ising_model
from qiskit.transpiler import CouplingMap
from qiskit.providers.aer import QasmSimulator
from qiskit import QuantumCircuit, execute

def run_circuit(circuit):
    ideal_simulator = QasmSimulator()

    # Execute and get counts
    result = execute(circuit, ideal_simulator, shots=50000).result()
    return result.get_counts(circuit)


decoded_file = decode_file('example_data_q4_q20')

for i, (arr, sol) in enumerate(decoded_file):
    
    if len(arr) != 8: continue

    if len(arr) not in [2**k for k in range(10)]:
        print('PASS')
        continue # only 2**k numbers of qubits allowed
        # 4, 8, 16 out of q4_to_q20

    S = np.array(arr)
    gamma = np.random.rand() * np.pi
    beta = np.random.rand() * np.pi

    J, h, bounds = get_ising_model(S)
    qaoa_circuit = get_circuit(gamma, beta, J, h)

    # e.g. coupling = [[0,1], [0,2], [1,2]]

    qubit_grid = get_qubit_grid(len(arr))

    coupling = CouplingMap()
    rows, cols = qubit_grid.shape
    grid_coupling = coupling.from_grid(rows, cols)

    swap_network_circuit = swap_network(qaoa_circuit, qubit_grid)
    basic_swap_circuit = swap_update(qaoa_circuit, grid_coupling, 0)
    lookahead_swap_circuit = swap_update(qaoa_circuit, grid_coupling, 1)
    stochastic_swap_circuit = swap_update(qaoa_circuit, grid_coupling, 2)
    sabre_swap_circuit = swap_update(qaoa_circuit, grid_coupling, 3) # Why is this not working???
    
    sim_ref = run_circuit(qaoa_circuit)
    sim_swap = run_circuit(swap_network_circuit)
    sim_basic = run_circuit(basic_swap_circuit)
    sim_look = run_circuit(lookahead_swap_circuit)
    sim_stoch = run_circuit(stochastic_swap_circuit)
    sim_sabre = run_circuit(sabre_swap_circuit)

    #results = [];
    #for (key, val) in sim_ref.items():
    #    
    #    arr = np.array([sim_swap.get(key, 0), sim_basic.get(key, 0),\
    #            sim_look.get(key, 0), sim_stoch.get(key, 0), sim_sabre.get(key, 0)])
    #    results.append(arr - val)

    #results = np.asarray(results)
    #print([np.sum(np.abs(results),axis=0)])

    #for (key, val) in sim_ref.items():

    #    print("{: <10} {: <10} {: <10}".format(val, sim_swap.get(key, 0),\
    #        int(abs(sim_swap.get(key, 0)-val) * 100 / val)))
    
    
    #print(qaoa_circuit)
    #print(swap_network_circuit)
    #print(basic_swap_circuit)
    #print(lookahead_swap_circuit)
    #print(stochastic_swap_circuit)
    #print(sabre_swap_circuit)

    print('swap network %d, basic swap %d, lookahead swap %d, stochastic swap %d, sabre swap %d' % \
        (swap_network_circuit.depth(), basic_swap_circuit.depth(), lookahead_swap_circuit.depth(), \
         stochastic_swap_circuit.depth(), sabre_swap_circuit.depth()))

    input()


