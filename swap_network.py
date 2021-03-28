import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag

def swap_positions(input_list, pos1, pos2):  
    input_list[pos1], input_list[pos2] = input_list[pos2], input_list[pos1] 
    return input_list

def do_all_ops(circuit, logical_qubit_grid, qubit_grid, operations):
    M,N = qubit_grid.shape
    
    didzz = False
    # The order is to reduce circuit depth
    # so do not simplify the for loops.
    for i in range(0,M-1,2):
        for j in range(N):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i+1,j]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i+1,j]
            didzz |= do_op(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(1,M-2,2):
        for j in range(N):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i+1,j]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i+1,j]
            didzz |= do_op(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(0,N-1,2):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i,j+1]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i,j+1]
            didzz |= do_op(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(1,N-2,2):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i,j+1]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i,j+1]
            didzz |= do_op(q1, q2, logical_q1, logical_q2, circuit, operations)

    return didzz


def do_op(q1, q2, logical_q1, logical_q2, circuit, operations):
    didzz = False

    if operations[logical_q1,logical_q2] != 0:
        do_zz_op(circuit, q1, q2, operations[logical_q1,logical_q2])
        didzz = True

    if operations[logical_q2,logical_q1] != 0:
        do_zz_op(circuit, q2, q1, operations[logical_q2,logical_q1])
        didzz = True

    operations[logical_q1,logical_q2] = 0
    operations[logical_q2,logical_q1] = 0

    return didzz

def do_zz_op(circuit, qubit1, qubit2, angle):
    #circuit.cx(qubit1,qubit2)
    #circuit.rz(angle,qubit2)
    #circuit.cx(qubit1,qubit2)
    circuit.rzz(angle, qubit1, qubit2)   

def qc_UL_swap(circuit, qubit_path, qubit_grid):
    N = len(qubit_path)
    qubit_grid_path = get_qubit_path(qubit_grid)

    for i in range(0,N-1,2):
        qubit_path = swap_positions(qubit_path, i, i+1)
        circuit.swap(qubit_grid_path[i], qubit_grid_path[i+1])

    return circuit 

def qc_UR_swap(circuit, qubit_path, qubit_grid):
    N = len(qubit_path)
    qubit_grid_path = get_qubit_path(qubit_grid)

    for i in range(1,N-1,2):
        qubit_path = swap_positions(qubit_path, i, i+1)
        circuit.swap(qubit_grid_path[i], qubit_grid_path[i+1])

    qubit_path = swap_positions(qubit_path, N-1, 0)
    circuit.swap(qubit_grid_path[N-1], qubit_grid_path[0])

    return circuit 

# WARNING: Returns a new circuit
def qc_UL_UR(input_circuit, logical_qubit_grid, qubit_grid, operations):
    circuit = input_circuit.copy()

    qubit_path = get_qubit_path(logical_qubit_grid)
    num_qubits = len(qubit_path)

    # optimization to reduce number of swaps
    zz_circuit = circuit.copy()
    zz_qubit_path = qubit_path.copy()

    for i in range(int(num_qubits / 2)):

        qc_UL_swap(circuit, qubit_path, qubit_grid)
        tmp_logical_qubit_grid = get_logical_grid(qubit_path, qubit_grid)

        if do_all_ops(circuit, tmp_logical_qubit_grid, qubit_grid, operations):
            zz_logical_grid = tmp_logical_qubit_grid.copy()
            zz_circuit = circuit.copy()

        qc_UR_swap(circuit, qubit_path, qubit_grid)
        tmp_logical_qubit_grid = get_logical_grid(qubit_path, qubit_grid)

        if do_all_ops(circuit, tmp_logical_qubit_grid, qubit_grid, operations):
            zz_logical_grid = tmp_logical_qubit_grid.copy()
            zz_circuit = circuit.copy()


    rows,cols = qubit_grid.shape

    # for loops needed to keep the old reference
    # to logical_qubit_grid and update callers value
    for i in range(rows):
        for j in range(cols):
            logical_qubit_grid[i, j] = zz_logical_grid[i, j]

    return zz_circuit

def qc_color_sep(circuit, logical_qubit_grid, qubit_grid): 
    m,n = qubit_grid.shape
    if m > n:
        for k in range(n):
            for i in range((k+1)%2,int(m/2),1):
                for j in range(i,m-i-1,2):
                    logical_qubit_grid = swap_positions(logical_qubit_grid, (j,k),(j+1,k))
                    circuit.swap(qubit_grid[j, k], qubit_grid[j + 1, k])   
    else: 
        for k in range(m):
            for i in range((k+1)%2,int(n/2),1):
                for j in range(i,n-i-1,2):
                    logical_qubit_grid = swap_positions(logical_qubit_grid, (k,j),(k,j+1))
                    circuit.swap(qubit_grid[k, j], qubit_grid[k, j + 1])   

def get_qubit_grid(num_qubits):
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

# WARNING: This only works if the circuit only
# contains ZZ and Rx gates, where all Rx gates
# are at the end.
def decompose_qaoa_circuit(circuit):
    N = circuit.num_qubits
    zz_ops = np.zeros((N,N))
    rx_ops = np.zeros(N)

    dag = circuit_to_dag(circuit)
    nodes = dag.gate_nodes()

    for node in nodes:

        if node.name == 'rzz':
            q1 = node.qargs[0].index
            q2 = node.qargs[1].index

            theta = node.op.params
            zz_ops[min(q1,q2),max(q1,q2)] += theta 

        elif node.name == 'rx':
            q1 = node.qargs[0].index

            theta = node.op.params
            rx_ops[q1] += theta
            
    return zz_ops, rx_ops

# WARNING: circuit has to have 2**k qubits
def swap_network(qaoa_circuit, qubit_grid=None):
    N = qaoa_circuit.num_qubits

    operations, rx_ops = decompose_qaoa_circuit(qaoa_circuit)
    print(operations)
    circuit = QuantumCircuit(N, N)
    circuit.h(range(N))

    if qubit_grid is None:
        qubit_grid = get_qubit_grid(N)

    def recurse(qubit_grid, logical_qubit_grid, circuit):
        do_all_ops(circuit, logical_qubit_grid, qubit_grid, operations)

        if qubit_grid.size == 2: return circuit
        if qubit_grid.size != 4: 
            circuit = qc_UL_UR(circuit, logical_qubit_grid, qubit_grid, operations)

        qc_color_sep(circuit, logical_qubit_grid, qubit_grid)

        logical_grid1, logical_grid2 = seperate_grid(logical_qubit_grid)
        grid1, grid2 = seperate_grid(qubit_grid)

        circuit = recurse(grid1, logical_grid1, circuit)
        circuit = recurse(grid2, logical_grid2, circuit)

        return circuit

    logical_qubit_grid = qubit_grid.copy()
    circuit = recurse(qubit_grid, logical_qubit_grid, circuit)  

    (r, c) = qubit_grid.shape

    for q, theta in enumerate(rx_ops):
        qq = logical_qubit_grid[int(np.floor(q / c)), q % c]
        circuit.rx(theta, qq)

    for q, theta in enumerate(rx_ops):
        qq = logical_qubit_grid[int(np.floor(q / c)), q % c]
        circuit.measure(q, qq)

    return circuit

