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

def do_all_ops(circuit, qubit_path, logical_qubit_grid, qubit_grid, operations):
    M,N = qubit_grid.shape
    for i in range(0,M-1,2):
        for j in range(N):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i+1,j]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i+1,j]
            do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(1,M-2,2):
        for j in range(N):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i+1,j]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i+1,j]
            do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(0,N-1,2):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i,j+1]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i,j+1]
            do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(1,N-2,2):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i,j+1]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i,j+1]
            do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

def do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations):
    if operations[logical_q1,logical_q2] != 0:
        do_zz_op(circuit, q1, q2, operations[logical_q1,logical_q2])

    if operations[logical_q2,logical_q1] != 0:
        do_zz_op(circuit, q2, q1, operations[logical_q2,logical_q1])

    operations[logical_q1,logical_q2] = 0
    operations[logical_q2,logical_q1] = 0

def do_zz_op(circuit, qubit1, qubit2, angle):
    circuit.cx(qubit1,qubit2)
    circuit.rz(angle,qubit2)
    circuit.cx(qubit1,qubit2)
    circuit.barrier()

def qc_UL_swap(circuit, qubit_path):
    N = len(qubit_path)
    for i in range(0,N-1,2):
        qubit_path = swapPositions(qubit_path, i, i+1)
        circuit.swap(i, i+1)
    return circuit, qubit_path 

def qc_UR_swap(circuit, qubit_path):
    N = len(qubit_path)
    for i in range(1,N-1,2):
        qubit_path = swapPositions(qubit_path, i, i+1)
        circuit.swap(i, i+1)
    circuit.swap(N-1, 0)
    qubit_path = swapPositions(qubit_path, N-1, 0)
    return circuit, qubit_path

def qc_UL_UR(circuit, qubit_path, qubit_grid, operations):
    num_qubits = len(qubit_path)
    for i in range(int(num_qubits/2)):
        qc_UL_swap(circuit, qubit_path)
        logical_qubit_grid = get_logical_grid(qubit_path, qubit_grid)
        do_all_ops(circuit, qubit_path, logical_qubit_grid, qubit_grid, operations)
        qc_UR_swap(circuit, qubit_path)
        logical_qubit_grid = get_logical_grid(qubit_path, qubit_grid)
        do_all_ops(circuit, qubit_path, logical_qubit_grid, qubit_grid, operations)

def qc_color_sep(circuit, qubit_grid): 
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

def get_logical_grid(qubit_path, qubit_grid):
    m,n = qubit_grid.shape
    logical_grid = np.zeros((m,n),int)
    logical_grid[0,:] = qubit_path[0:n]

    for i in range(1,m):
        vec = qubit_path[(i-1)*(n-1) + n:i*(n-1) + n]
        
        if i%2 == 0:
            logical_grid[i,1:] = vec
        else:
            logical_grid[i,1:] = np.flip(vec)
    logical_grid[1:,0] = np.flip(qubit_path[m*n-(m-1):m*n])
    return logical_grid    

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
    logical_qubit_grid = qubit_grid.copy()
    
    def recurse(logical_qubit_grid, qubit_grid):       
        qubit_path = get_qubit_path(logical_qubit_grid)
        do_all_ops(circuit, qubit_path, logical_qubit_grid, qubit_grid, operations)
        if qubit_grid.size == 2: return
        if qubit_grid.size != 4: 
            qc_UL_UR(circuit, qubit_path, qubit_grid, operations)

        qubit_grid_color_seperated = logical_qubit_grid.copy()
        qc_color_sep(circuit, qubit_grid_color_seperated)        
        logical_grid1, logical_grid2 = seperate_grid(qubit_grid_color_seperated)
        grid1, grid2 = seperate_grid(qubit_grid)
        
        recurse(logical_grid1, grid1)
        recurse(logical_grid2, grid2)

    recurse(logical_qubit_grid, qubit_grid)  
    circuit.barrier()
    circuit.rx(2*beta, range(N))
    print(operations)
    return circuit

