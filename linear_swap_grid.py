import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from decompose_circuit import decompose_qaoa_circuit

def swap_positions(input_list, pos1, pos2): 
    if input_list[pos1] >= 0 and input_list[pos2] >= 0:
        input_list[pos1], input_list[pos2] = input_list[pos2], input_list[pos1] 
    return input_list

def do_all_ops(circuit, logical_qubit_grid, qubit_grid, operations):
    M,N = qubit_grid.shape
    num_qubits = circuit.num_qubits
    didzz = False
    # The order is to reduce circuit depth
    # so do not simplify the for loops.
    
    for i in range(0,M-1,2):
        for j in range(N):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i+1,j]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i+1,j]
            if q1 >= 0 and q2 >= 0 and logical_q1 >= 0 and logical_q2 >= 0:
                didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(1,M-1,2):
        for j in range(N):

            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i+1,j]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i+1,j]
            if q1 >= 0 and q2 >= 0 and logical_q1 >= 0 and logical_q2 >= 0:
                didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(0,N-1,2):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i,j+1]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i,j+1]
            if q1 >= 0 and q2 >= 0 and logical_q1 >= 0 and logical_q2 >= 0:
                didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(1,N-1,2):
            logical_q1 = logical_qubit_grid[i,j]
            logical_q2 = logical_qubit_grid[i,j+1]
            q1 = qubit_grid[i,j]
            q2 = qubit_grid[i,j+1]
            if q1 >= 0 and q2 >= 0 and logical_q1 >= 0 and logical_q2 >= 0:
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
    circuit.rzz(angle, qubit1, qubit2)   

def qc_UL_swap(circuit, logical_qubit_path, qubit_path, operations):
    N = len(qubit_path)

    for i in range(0,N-1,2):
        logical_qubit_path = swap_positions(logical_qubit_path, i, i+1)
        circuit.swap(qubit_path[i], qubit_path[i+1])
    return circuit 

def qc_UR_swap(circuit, logical_qubit_path, qubit_path, operations):
    N = len(qubit_path)

    for i in range(1,N-1,2):
        logical_qubit_path = swap_positions(logical_qubit_path, i, i+1)
        circuit.swap(qubit_path[i], qubit_path[i+1])
    return circuit 

# WARNING: Returns a new circuit
def qc_UL_UR(input_circuit, logical_qubit_path, qubit_path, qubit_grid, operations):

    circuit = input_circuit.copy()
    num_qubits = circuit.num_qubits
    if not np.any(operations):
        return circuit
    for i in range(int(num_qubits/2)):
        
        if np.any(operations):
            qc_UL_swap(circuit, logical_qubit_path, qubit_path, operations)
            logical_qubit_grid = get_logical_grid(logical_qubit_path)
        do_all_ops(circuit, logical_qubit_grid, qubit_grid, operations)
        
        if np.any(operations):
            qc_UR_swap(circuit, logical_qubit_path, qubit_path, operations)
            logical_qubit_grid = get_logical_grid(logical_qubit_path)
        do_all_ops(circuit, logical_qubit_grid, qubit_grid, operations)
    return circuit



def get_qubit_grid(num_qubits):
    n = round(math.sqrt(num_qubits))
    m = num_qubits/n
    count = 0

    vec = np.zeros((int(np.ceil(m)),n))
    for i in range(int(np.ceil(m))):
        for j in range(n):
            if count < num_qubits:
                if i%2 == 0:
                    vec[i][j] = count
                else: 
                    vec[i][n-j-1] = count
                count = count + 1
            else: 
                if i%2 == 0:
                    vec[i][j] = -1
                else: 
                    vec[i][n-j-1] = -1
                count = count + 1
    return vec.astype(int)

def get_qubit_path(qubit_grid):
    m,n =  qubit_grid.shape
    #qubit_path = np.flip(qubit_grid[m-1,:])
    qubit_path = np.array([])

    for i in range(m-1,-1, -1):
            vec_reverse = np.flip(qubit_grid[i,:])
            if i%2 == 0:
                qubit_path = np.append(qubit_path, vec_reverse)
            else:
                qubit_path = np.append(qubit_path, qubit_grid[i,:])
    return qubit_path.astype(int)

def get_logical_grid(logical_qubit_path):
    num_qubits = len(logical_qubit_path)
    n = round(math.sqrt(num_qubits))
    m = num_qubits/n
    count = 0

    vec = np.zeros((int(np.ceil(m)),n))
    for i in range(int(np.ceil(m))):
        for j in range(n):
            if count < num_qubits:
                if i%2 == 0:
                    vec[i][j] = logical_qubit_path[count]
                else: 
                    vec[i][n-j-1] = logical_qubit_path[count]
                count = count + 1
            else: 
                if i%2 == 0:
                    vec[i][j] = -1
                else: 
                    vec[i][n-j-1] = -1
                count = count + 1
    return vec.astype(int)


def linear_swap_method(qaoa_circuit, p, qubit_path=None):
    N = qaoa_circuit.num_qubits
    operations, rz_ops, rx_ops = decompose_qaoa_circuit(qaoa_circuit, N, p)
    circuit = QuantumCircuit(N, N)
    circuit.h(range(N))
    if qubit_path is None:
        qubit_path = np.array(range(N))
    logical_qubit_path = qubit_path.copy()
    
    qubit_grid = get_qubit_grid(N)


    for i in range(p):
        logical_qubit_grid = get_logical_grid(logical_qubit_path)
        do_all_ops(circuit, logical_qubit_grid, qubit_grid, operations[i,:,:])
        circuit = qc_UL_UR(circuit, logical_qubit_path, qubit_path, qubit_grid, operations[i,:,:])
        
        for q, theta in enumerate(rz_ops[i,:]):
            qq = logical_qubit_path[q]
            circuit.rz(theta, qq)

        for q, theta in enumerate(rx_ops[i,:]):
            qq = logical_qubit_path[q]
            circuit.rx(theta, qq)
        
    for q, theta in enumerate(rx_ops[0,:]):
        qq = logical_qubit_path[q]
        circuit.measure(q, qq)

    return circuit