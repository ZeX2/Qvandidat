import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag

def swapPositions(list, pos1, pos2):  
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

def UL_swap(array):
    N = len(array)
    for i in range(0,N-1,2):
        array = swapPositions(array, i, i+1)
    return array 

def UR_swap(array):
    N = len(array)
    for i in range(1,N-2,2):
        array=swapPositions(array, i+1, i+2)
    return array 

def do_all_ops(circuit, grid_shape, qubit_line, qubit_path, operations):
    print('zzz')
    print(circuit)
    M,N = grid_shape
    
    didzz = False
    # The order is to reduce circuit depth
    # so do not simplify the for loops.
    for i in range(0,M-1,2):
        for j in range(N):
            print(i+1, j, '|', i, j)
            k1 = i * N + j
            k2 = (i + 1) * N + j
            print(k1, k2)
            logical_q1 = qubit_path[k1]
            logical_q2 = qubit_path[k2]
            q1 = qubit_line[k1]
            q2 = qubit_line[k2]
            didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(1,M-2,2):
        for j in range(N):
            print(i+1, j, '|', i, j)
            k1 = i * N + j
            k2 = (i + 1) * N + j
            print(k1, k2)
            logical_q1 = qubit_path[k1]
            logical_q2 = qubit_path[k2]
            q1 = qubit_line[k1]
            q2 = qubit_line[k2]
            didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(0,N-1,2):
            print(i, j+1, '|', i, j)
            k1 = i * N + j
            k2 = i * N + j + 1
            print(k1, k2)
            logical_q1 = qubit_path[k1]
            logical_q2 = qubit_path[k2]
            q1 = qubit_line[k1]
            q2 = qubit_line[k2]
            didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(M):
        for j in range(1,N-2,2):
            print(i, j+1, '|', i, j)
            k1 = i * N + j
            k2 = i * N + j + 1
            print(k1, k2)
            logical_q1 = qubit_path[k1]
            logical_q2 = qubit_path[k2]
            q1 = qubit_line[k1]
            q2 = qubit_line[k2]
            didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)
    
    print('yyyy')

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

    #print('zz \\w', qubit1, 'and', qubit2)

def qc_UL_swap(circuit, qubit_path, qubit_line):
    N = len(qubit_path)

    for i in range(0,N-1,2):
        qubit_path = swapPositions(qubit_path, i, i+1)
        circuit.swap(qubit_line[i], qubit_line[i+1])
    return circuit 

def qc_UR_swap(circuit, qubit_path, qubit_line):
    N = len(qubit_path)
    for i in range(1,N-1,2):
        qubit_path = swapPositions(qubit_path, i, i+1)
        circuit.swap(qubit_line[i], qubit_line[i+1])
    return circuit 

def qc_UL_UR(input_circuit, grid_shape, qubit_line, qubit_path, operations):

    circuit = input_circuit.copy()
    num_qubits = len(qubit_path)

    for i in range(int(num_qubits/2)):
        
        if np.any(operations):
            qc_UL_swap(circuit, qubit_path, qubit_line)
        do_all_ops(circuit, grid_shape, qubit_line, qubit_path, operations)
        
        if np.any(operations):
            qc_UR_swap(circuit, qubit_path, qubit_line)
        do_all_ops(circuit, grid_shape, qubit_line, qubit_path, operations)
    return circuit


def get_operations(J, gamma):
    N = len(J)
    operations = np.zeros(J.shape)
    for i in range(N):
        for j in range(i):
            operations[i,j] = 2*gamma*J[i,j]
    return operations.T

#def decompose_qaoa_circuit_old(circuit):
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

def decompose_qaoa_circuit(circuit,N,p):
    zz_ops = np.zeros((p,N,N))
    rx_ops = np.zeros((p,N))

    dag = circuit_to_dag(circuit)
    nodes = dag.gate_nodes()
    i = 0
    j = 0
    operations_order = np.empty(0)
    for node in nodes:
        if node.name == 'rzz':
            operations_order = np.append(operations_order, 'rzz')
            i = i+1
            if operations_order[i-2] == 'rx' and operations_order[i-1] == 'rzz':
                j = j+1
            q1 = node.qargs[0].index
            q2 = node.qargs[1].index

            theta = node.op.params
            zz_ops[j,min(q1,q2),max(q1,q2)] += theta 
        elif node.name == 'rx':
            operations_order = np.append(operations_order, 'rx')
            i = i+1
            q1 = node.qargs[0].index
            theta = node.op.params
            rx_ops[j,q1] += theta
    return zz_ops, rx_ops


def linear_swap_method(qaoa_circuit, grid_shape, p, qubit_line=None):
    N = qaoa_circuit.num_qubits
    operations, rx_ops = decompose_qaoa_circuit(qaoa_circuit, N, p)
    circuit = QuantumCircuit(N, N)
    circuit.h(range(N))
    
    if qubit_line is None:
        qubit_line = np.array(range(N))
    qubit_path = qubit_line.copy()
    
    for i in range(p):
        do_all_ops(circuit, grid_shape, qubit_line, qubit_path, operations[i,:,:])
        circuit = qc_UL_UR(circuit, grid_shape, qubit_line, qubit_path, operations[i,:,:])
        
        for q, theta in enumerate(rx_ops[i,:]):
            qq = qubit_path[q]
            circuit.rx(theta, qq)

    for q, theta in enumerate(rx_ops[0,:]):
        qq = qubit_path[q]
        circuit.measure(q, qq)

    return circuit

def simplify(circuit):
    return transpile(circuit, basis_gates=['cx', 'rz', 'rx', 'swap'], optimization_level=3)

