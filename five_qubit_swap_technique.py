import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag

def swap_positions(input_list, pos1, pos2):
    input_list[pos1], input_list[pos2] = input_list[pos2], input_list[pos1] 
    return input_list

def decompose_qaoa_circuit(circuit,p):
    N = circuit.num_qubits
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

def do_all_ops(circuit, coupling, qubit_order, operations):
    N = circuit.num_qubits
    didzz = False
    # The order is to reduce circuit depth
    # so do not simplify the for loops.

    if N == 2:
        q1 = 0
        q2 = 1
        didzz |= do_op(q1, q2, q1, q2, circuit, operations)
        return didzz
    logical_q1 = qubit_in_the_middle(coupling)
    q1 = N-1
    for i in range(N):
        logical_q2 = i
        q2 = np.where(qubit_order == logical_q2)[0][0]
        didzz |= do_op(q1, q2, logical_q1, logical_q2, circuit, operations)
    return didzz

def do_op(q1, q2, logical_q1, logical_q2, circuit, operations):
    didzz = False

    if operations[logical_q1,logical_q2] != 0 and q1 != q2:
        do_zz_op(circuit, q1, q2, operations[logical_q1,logical_q2])
        didzz = True

    if operations[logical_q2,logical_q1] != 0 and q1 != q2:
        do_zz_op(circuit, q2, q1, operations[logical_q2,logical_q1])
        didzz = True

    operations[logical_q1,logical_q2] = 0
    operations[logical_q2,logical_q1] = 0
    return didzz

def do_zz_op(circuit, qubit1, qubit2, angle):
    circuit.rzz(angle, qubit1, qubit2)   

def qubit_in_the_middle(coupling):
    c = np.array([])
    for i in range(len(coupling)):
        c = np.concatenate((c, [coupling[i][0]]))
        c = np.concatenate((c, [coupling[i][1]]))
    counts = np.bincount(c.astype(int))
    return np.argmax(counts)

def swap(circuit, coupling, qubit_order, operations):
    N = circuit.num_qubits
    for i in range(N-2):
        q_mid = qubit_in_the_middle(coupling)
        circuit.swap(i, N-1)

        qubit_order = swap_positions(qubit_order, i, N-1)
        for j in range(0,len(coupling),2):
            if j != 2*i and j != 2*i+1:
                if coupling[j][0] == q_mid:
                    coupling[j][0] = qubit_order[-1]
                    coupling[j+1][1] = qubit_order[-1]
                else:
                    coupling[j][1] = qubit_order[-1]
                    coupling[j+1][0] = qubit_order[-1]

            do_all_ops(circuit, coupling, qubit_order, operations)

        if np.all((operations == 0)):
            continue
    return circuit

def star_swap(qaoa_circuit, p, coupling = None):
    N = qaoa_circuit.num_qubits
    circuit = QuantumCircuit(N,N)
    circuit.h(range(N))
    zz_ops, rx_ops = decompose_qaoa_circuit(qaoa_circuit, p)
    print(zz_ops)
    print(rx_ops)
    if coupling is None:
        coupling = []
        # Last qubit in the middle
        for i in range(N-1):
            coupling = coupling + [[i,N-1]] + [[N-1,i]]
    qubit_order = np.array(range(N))

    for i in range(p):
        if N != 1:
            do_all_ops(circuit, coupling, qubit_order, zz_ops[i,:,:])
        
            circuit = swap(circuit, coupling, qubit_order, zz_ops[i,:,:])

        for q, theta in enumerate(rx_ops[i,:]):
            qq = qubit_order[q]
            if theta != 0:
                circuit.rx(theta, qq) 
     
    for q in range(N):
        qq = qubit_order[q]
        circuit.measure(q,qq)

    return circuit