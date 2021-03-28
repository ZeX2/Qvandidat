import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager, passes, CouplingMap, Layout
from qiskit.converters import circuit_to_dag
from qiskit.transpiler.passes import(
    Unroller, 
    BasicSwap, 
    LookaheadSwap, 
    StochasticSwap, 
    SabreSwap, 
    TrivialLayout,
    DenseLayout,
    NoiseAdaptiveLayout) 


def change_bases(circuit, bases):
    pass_ = Unroller(bases)
    pm = PassManager(pass_)
    new_circuit = pm.run(circuit)
    return new_circuit


def swap_update(circuit, coupling_map, n):
    if n not in range(1, 5):
        return print('SWAP performance not defined')

    if type(coupling_map) is not CouplingMap:
        coupling_map = CouplingMap(couplinglist=coupling_map)

    if n == 1:
        bs = BasicSwap(coupling_map=coupling_map)
        pass_manager = PassManager(bs)
        basic_circ = pass_manager.run(circuit)
        return basic_circ
    elif n == 2:
        ls = LookaheadSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ls)
        lookahead_circ = pass_manager.run(circuit)
        return lookahead_circ
    elif n == 3:
        ss = StochasticSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ss)
        stochastic_circ = pass_manager.run(circuit)
        return stochastic_circ
    elif n == 4:
        ss = SabreSwap(coupling_map=coupling_map)
        pass_manager = PassManager(ss)
        sabre_circ = pass_manager.run(circuit)
        return sabre_circ

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

def do_all_ops(circuit, logical_qubit_grid, qubit_grid, operations):
    M,N = qubit_grid.shape

    print('logical grid, then grid')
    print(logical_qubit_grid)
    print(qubit_grid)
    
    didzz = False

    # The order is to reduce circuit depth
    # so do not simplify the for loops because
    # 
    for i in range(0,M-1,2):
        for j in range(N):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i+1,j]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i+1,j]
            didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(1,M-2,2):
        for j in range(N):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i+1,j]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i+1,j]
            didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(0,N-1,2):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i,j+1]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i,j+1]
            didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(1,N-2,2):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i,j+1]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i,j+1]
            didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    return didzz

def do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations):
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
    #circuit.barrier()
    circuit.rzz(angle,qubit1,qubit2)
    #circuit.barrier()

def do_zz_op2(circuit, qubit1, qubit2, angle):
    #circuit.barrier()
    circuit.cx(qubit1,qubit2)
    circuit.rz(angle,qubit2)
    circuit.cx(qubit1,qubit2)
    #circuit.barrier()

    print('zz \\w', qubit1, 'and', qubit2)

def qc_UL_swap(circuit, qubit_path, qubit_grid):
    N = len(qubit_path)
    qubit_grid_path = get_qubit_path(qubit_grid)

    for i in range(0,N-1,2):
        qubit_path = swapPositions(qubit_path, i, i+1)
        circuit.swap(qubit_grid_path[i], qubit_grid_path[i+1])

    return circuit 

def qc_UR_swap(circuit, qubit_path, qubit_grid):
    N = len(qubit_path)
    qubit_grid_path = get_qubit_path(qubit_grid)

    for i in range(1,N-1,2):
        qubit_path = swapPositions(qubit_path, i, i+1)
        circuit.swap(qubit_grid_path[i], qubit_grid_path[i+1])

    # The following line was outcommented, but I think it is needed.
    qubit_path = swapPositions(qubit_path, N-1, 0)
    circuit.swap(qubit_grid_path[N-1], qubit_grid_path[0])

    return circuit 

def qc_UL_UR(input_circuit, logical_qubit_grid, qubit_grid, operations):
    circuit = input_circuit.copy()

    qubit_path = get_qubit_path(logical_qubit_grid)
    num_qubits = len(qubit_path)

    zz_circuit = circuit.copy()
    zz_qubit_path = qubit_path.copy()

    for i in range(int(num_qubits / 2)):
        print('CIRCUIT QC UR UL')
        print(circuit)

        qc_UL_swap(circuit, qubit_path, qubit_grid)
        tmp_logical_qubit_grid = get_logical_grid(qubit_path, qubit_grid)

        if do_all_ops(circuit, tmp_logical_qubit_grid, qubit_grid, operations):
            zz_logical_grid = tmp_logical_qubit_grid.copy()
            zz_circuit = circuit.copy()

        print('CIRCUIT QC UR UL')
        print(circuit)

        qc_UR_swap(circuit, qubit_path, qubit_grid)
        tmp_logical_qubit_grid = get_logical_grid(qubit_path, qubit_grid)

        if do_all_ops(circuit, tmp_logical_qubit_grid, qubit_grid, operations):
            zz_logical_grid = tmp_logical_qubit_grid.copy()
            zz_circuit = circuit.copy()


    rows,cols = qubit_grid.shape

    for i in range(rows):
        for j in range(cols):
            logical_qubit_grid[i, j] = zz_logical_grid[i, j]

    print('LEAVING QC UL UR')
    print(zz_logical_grid)
    print(logical_qubit_grid)
    print(qubit_grid)

    return zz_circuit

def qc_color_sep(circuit, logical_qubit_grid, qubit_grid): 
    m,n = qubit_grid.shape
    if m > n:
        for k in range(n):
            for i in range((k+1)%2,int(m/2),1):
                for j in range(i,m-i-1,2):
                    logical_qubit_grid = swapPositions(logical_qubit_grid, (j,k),(j+1,k))
                    #circuit.swap(k + j * n, k + 1 + j * n)
                    circuit.swap(qubit_grid[j, k], qubit_grid[j + 1, k])   
    else: 
        for k in range(m):
            for i in range((k+1)%2,int(n/2),1):
                for j in range(i,n-i-1,2):
                    logical_qubit_grid = swapPositions(logical_qubit_grid, (k,j),(k,j+1))
                    #circuit.swap(j + k * n, j + 1 + k * n)   
                    circuit.swap(qubit_grid[k, j], qubit_grid[k, j + 1])   

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


# J and qubit_grid has to have 2**k qubits
def swap_network(qaoa_circuit, qubit_grid=None):
    N = qaoa_circuit.num_qubits

    operations, rx_ops = decompose_qaoa_circuit(qaoa_circuit)
    print(operations)
    circuit = QuantumCircuit(N, N)
    circuit.h(range(N))
    #circuit.barrier()

    if qubit_grid is None:
        qubit_grid = get_qubit_grid(N)

    def recurse(qubit_grid, logical_qubit_grid, circuit):
        # Because qc_UL_UR returns a circuit and circuit is defined before recurse

        do_all_ops(circuit, logical_qubit_grid, qubit_grid, operations)

        if qubit_grid.size == 2: return circuit
        if qubit_grid.size != 4: 

            print('CIRCUIT BEFORE')
            print(circuit)

            circuit = qc_UL_UR(circuit, logical_qubit_grid, qubit_grid, operations)
            print('FROM QC UL UR')
            print(logical_qubit_grid)
            print(qubit_grid)
            print('CIRCUIT AFTER')
            print(circuit)

        # I don't think copy is needed here. If not; it also enables
        # us took keep track of logical_qubit_grid globally
        #qubit_grid_color_separated = logical_qubit_grid.copy()
        qubit_grid_color_separated = logical_qubit_grid
        qc_color_sep(circuit, qubit_grid_color_separated, qubit_grid)

        logical_grid1, logical_grid2 = seperate_grid(qubit_grid_color_separated)
        grid1, grid2 = seperate_grid(qubit_grid)
        
        print('recurse logical grids')
        print(logical_grid1)
        print(qubit_grid_color_separated)

        circuit = recurse(grid1, logical_grid1, circuit)
        circuit = recurse(grid2, logical_grid2, circuit)

        return circuit

    logical_qubit_grid = qubit_grid.copy()
    circuit = recurse(qubit_grid, logical_qubit_grid, circuit)  
  
    #circuit.barrier()

    print('SEE ME')
    print(logical_qubit_grid)

    (r, c) = qubit_grid.shape

    for q, theta in enumerate(rx_ops):
        qq = logical_qubit_grid[int(np.floor(q / c)), q % c]
        circuit.rx(theta, qq)
        print('QQQ', qq, q, q%c, int(np.floor(q / c)))

    for q, theta in enumerate(rx_ops):
        qq = logical_qubit_grid[int(np.floor(q / c)), q % c]
        circuit.measure(q, qq)

    print(operations)

    return circuit


def simplify(circuit):
    return transpile(circuit, basis_gates=['cx', 'rz', 'rx', 'swap'], optimization_level=3)

