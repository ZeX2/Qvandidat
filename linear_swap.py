import numpy as np
import math
from qiskit import QuantumCircuit

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
    for i in range(0,N-2,2):
        array=swapPositions(array, i+1, i+2)
    return array 

def do_all_ops(circuit, logical_qubit_path, qubit_path, operations):
    didzz = False
    M = len(logical_qubit_path)
    # The order is to reduce circuit depth
    # so do not simplify the for loops because
    # 
    for i in range(0,M-1,2):
        logical_q1 = logical_qubit_path[i]
        logical_q2 = logical_qubit_path[i+1]
        q1 = qubit_path[i]
        q2 = qubit_path[i+1]
        didzz |= do_op_new(q1, q2, logical_q1, logical_q2, circuit, operations)

    for i in range(1,M-2,2):
        logical_q1 = logical_qubit_path[i]
        logical_q2 = logical_qubit_path[i+1]
        q1 = qubit_path[i]
        q2 = qubit_path[i+1]
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

def qc_UL_swap(circuit, qubit_path):
    N = len(qubit_path)

    for i in range(0,N-1,2):
        qubit_path = swapPositions(qubit_path, i, i+1)
        circuit.swap(qubit_path[i], qubit_path[i+1])
    return circuit 

def qc_UR_swap(circuit, qubit_path):
    N = len(qubit_path)
    for i in range(1,N-1,2):
        qubit_path = swapPositions(qubit_path, i, i+1)
        circuit.swap(qubit_path[i], qubit_path[i+1])
    return circuit 

def qc_UL_UR(input_circuit, qubit_path, operations):
    circuit = input_circuit.copy()
    num_qubits = len(qubit_path)

    for i in range(int(num_qubits/2)):
        qc_UL_swap(circuit, qubit_path)
        logical_qubit_path = qubit_path.copy()
        do_all_ops(circuit, logical_qubit_path, qubit_path, operations)
        print(qubit_path)
        qc_UR_swap(circuit, qubit_path)
        logical_qubit_path = qubit_path.copy()
        print(logical_qubit_path)
        print(qubit_path)
        do_all_ops(circuit, logical_qubit_path, qubit_path, operations)
    return circuit


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


# J and qubit_path has to have 2**k qubits
def linear_swap_method(J, gamma, beta):
    N = len(J)
    operations = get_operations(J, gamma)
    print(operations)
    circuit = QuantumCircuit(N)
    circuit.h(range(N))
    circuit.barrier()

    qubit_path = np.array(range(N))
    logical_qubit_path = qubit_path.copy()
    

    do_all_ops(circuit, logical_qubit_path, qubit_path, operations)
    new_circ = qc_UL_UR(circuit, qubit_path, operations)

    new_circ.barrier()
    new_circ.rx(2*beta, range(N))
    print(operations)
    return new_circ


def simplify(circuit):
    return transpile(circuit, basis_gates=['cx', 'rz', 'rx', 'swap'], optimization_level=3)

