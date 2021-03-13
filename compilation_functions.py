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


def swap_update(circuit, coupling, int):
    if (int != 1 and int != 2 and int != 3):
        return print('SWAP performance not defined')
    coupling_map = CouplingMap(couplinglist=coupling)
    if int == 1:
        bs = BasicSwap(coupling_map=coupling_map)
        pass_manager = PassManager(bs)
        basic_circ = pass_manager.run(circuit)
        return basic_circ
    elif int == 2:
        ls = LookaheadSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ls)
        lookahead_circ = pass_manager.run(circuit)
        return lookahead_circ
    elif int == 3:
        ss = StochasticSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ss)
        stochastic_circ = pass_manager.run(circuit)
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

def rotatex(qubit, angle):
    qubit.ry(np.pi/2)
    qubit.rz(angle)
    qubit.ry(np.pi/2)
    return qubit

def swapPositions(list, pos1, pos2):  
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

def UL(array):
    N = len(array)
    for i in range(0,N-1,2):
        array = swapPositions(array, i, i+1)
    return array 

def UR(array):
    N = len(array)
    for i in range(0,N,2):
        if (i+1< N-1):
            array=swapPositions(array, i+1, i+2)
        else:
            array=swapPositions(array, i+1, 0)
    return array 

def swap_all_pos_shifted(array):
    N = len(array)
    for i in range(1,int(N/2),1):
        for j in range(i,N-i-1,2):
            array = swapPositions(array, j, j+1)
    return array

def swap_all_pos(array):
    N = len(array)
    for i in range(0,int(N/2),1):
        for j in range(i,N-i-1,2):
            array = swapPositions(array, j, j+1)
    return array

def color_sep(matrix):
    m,n = matrix.shape
    for i in range(m):
        if i%2 == 0:
            matrix[i] = swap_all_pos_shifted(matrix[i])
        else:
            matrix[i] = swap_all_pos(matrix[i])
    return matrix

def do_ops(i, circuit, qubit_map, operations):
    j = qubit_map[i]
    k = qubit_map[(i+1) % len(qubit_map)]
    i1 = (i+1)%len(qubit_map)
    j, k = min(j, k), max(j, k) # cx i och i1 byt plats också

    if operations[j,k] != 0:
        circuit.cx(i,i1)
        circuit.rz(operations[j,k],i1)
        circuit.cx(i,i1)
    operations[j,k] = 0
    circuit.swap(i,i1)
    return circuit

def qc_UL(circuit, qubit_map, operations):
    N = len(qubit_map)
    for i in range(0,N-1,2):
        circuit = do_ops(i, circuit, qubit_map, operations)
        qubit_map = swapPositions(qubit_map, i, i+1)
    return circuit 

def qc_UR(circuit, qubit_map, operations):
    N = len(qubit_map)
    for i in range(1,N-1,2):
        circuit = do_ops(i, circuit, qubit_map, operations)
        qubit_map = swapPositions(qubit_map, i, i+1)
    circuit.swap(N-1, 0)
    qubit_map = swapPositions(qubit_map, N-1, 0)
    return circuit 


def qc_color_sep(circuit, qubit_grid): #
    m,n = qubit_grid.shape
    if m > n:
        qubit_grid = qubit_grid.T
        for k in range(n):
            for i in range((k+1)%2,int(m/2),1):
                for j in range(i,m-i-1,2):
                    qubit_grid = swapPositions(qubit_grid, (k,j),(k,j+1))
                    circuit.swap(k + j * n, k + 1 + j * n)
        qubit_grid = qubit_grid.T
    else: 
        for k in range(m):
            for i in range((k+1)%2,int(n/2),1):
                for j in range(i,n-i-1,2):
                    qubit_grid = swapPositions(qubit_grid, (k,j),(k,j+1))
                    circuit.swap(j + k * n, j + 1 + k * n)   

def get_qubit_grid(num_qubits): #
    vec = np.array(range(num_qubits))
    if num_qubits%10 == 2 or num_qubits%10 == 8:
        m = int(math.sqrt(num_qubits/2))
        n = int(math.sqrt(num_qubits/2)*2)
    else:
        m = int(math.sqrt(num_qubits))
        n = int(math.sqrt(num_qubits))
    return vec.reshape(m,n)

def qc_UL_UR(circuit, qubit_map, operations):
    num_qubits = len(qubit_map)
    for i in range(num_qubits):
        do_ops(i, circuit, qubit_map, operations)
    for i in range(int(num_qubits/2)):
        qc_UL(circuit, qubit_map, operations)
        qc_UR(circuit, qubit_map, operations)

def get_qubit_path(qubit_grid):
    m,n = qubit_grid.shape
    grid_path = qubit_grid[0, 0:]
    for i in range(1,m):
        vec_reverse = np.flip(qubit_grid[i,1:])
        if i%2 == 0:
            grid_path = np.append(grid_path, qubit_grid[i,1:])
        else:
            grid_path = np.append(grid_path, vec_reverse)
    return np.append(grid_path, np.flip(qubit_grid[1:,0].T))

def seperate_grid(qubit_grid):
    m,n = qubit_grid.shape
    m_range = int(m/2)
    n_range = int(n/2)
    if m > n:
        new_grid1 = qubit_grid[0:m_range,0:n]
        new_grid2 = qubit_grid[m_range:m,0:n]
        return (new_grid1, new_grid2)
    else:
        new_grid1 = qubit_grid[0:m,0:n_range]
        new_grid2 = qubit_grid[0:m,n_range:n]
        return (new_grid1, new_grid2)    

def get_operations(J, gamma):
    N = len(J)
    operations = np.zeros(J.shape)
    for i in range(N):
            for j in range(i):
                operations[i,j] = 2*gamma*J[i,j]
    return operations.T

def swap_network(J, gamma, beta):
    N = len(J)
    operations = get_operations(J, gamma)
    print(operations)
    circuit = QuantumCircuit(N)
    circuit.barrier()
    qubit_grid = get_qubit_grid(N)

    def recurse(qubit_grid):
        if qubit_grid.size == 1: return
        
        qubit_path = get_qubit_path(qubit_grid)
        qc_UL_UR(circuit, qubit_path,operations)
        qc_color_sep(circuit, qubit_grid)
        grid1, grid2 = seperate_grid(qubit_grid)
    
        recurse(grid1)
        recurse(grid2)

    recurse(qubit_grid)    
    circuit.barrier()
    circuit.rx(2*beta, range(N))
    print(operations)

    return circuit
