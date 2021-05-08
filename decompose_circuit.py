# Method to decompose a quantum circuit with rzz, rz and rx gates
# The gate order in the circuit has to be rzz, rz, rx

import numpy as np
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag


def decompose_qaoa_circuit(circuit,N,p):
    zz_ops = np.zeros((p,N,N))
    rz_ops = np.zeros((p,N))
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

        elif node.name == 'rz':
            operations_order = np.append(operations_order, 'rz')
            i = i+1
            q1 = node.qargs[0].index
            theta = node.op.params
            rz_ops[j,q1] += theta

        elif node.name == 'rx':
            operations_order = np.append(operations_order, 'rx')
            i = i+1
            q1 = node.qargs[0].index
            theta = node.op.params
            rx_ops[j,q1] += theta

    return zz_ops, rz_ops, rx_ops