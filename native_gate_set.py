import numpy as np
import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.dagcircuit import DAGCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.circuit.library import RYGate, RZGate, CXGate, CZGate,\
        HGate, iSwapGate, RXGate

# Should be eqvivalent to:
#circuit.ry(-np.pi/2)
#circuit.rz(angle)
#circuit.ry(np.pi/2)
def get_rx_dag(angle):
    dag = DAGCircuit()
    q = QuantumRegister(1, "q")

    dag.add_qreg(q)
    dag.apply_operation_back(RYGate(-np.pi/2), qargs=q)
    dag.apply_operation_back(RZGate(angle), qargs=q)
    dag.apply_operation_back(RYGate(np.pi/2), qargs=q)
    
    return dag

def get_zz_dag(angle):
    dag = DAGCircuit()
    q = QuantumRegister(2, "q")

    dag.add_qreg(q)

    dag.compose(get_h_dag(), qubits=[q[1]])
    #dag.apply_operation_back(HGate(), qargs=[q[1]])
    dag.apply_operation_back(CZGate(), qargs=[q[0], q[1]])

    dag.compose(get_rx_dag(angle), qubits=[q[1]])
    #dag.apply_operation_back(RXGate(angle), qargs=[q[1]])

    dag.apply_operation_back(CZGate(), qargs=[q[0], q[1]])
    dag.compose(get_h_dag(), qubits=[q[1]])
    #dag.apply_operation_back(HGate(), qargs=[q[1]])

    return dag

def get_h_dag():
    dag = DAGCircuit()
    q = QuantumRegister(1, "q")

    dag.add_qreg(q)
    dag.apply_operation_back(RZGate(np.pi), qargs=q)
    dag.apply_operation_back(RYGate(np.pi/2), qargs=q)
    
    return dag

def get_swap_dag():

    dag = DAGCircuit()
    q = QuantumRegister(2, "q")

    dag.add_qreg(q)

    dag.compose(get_h_dag(), qubits=[q[0]])
    #dag.apply_operation_back(HGate(), qargs=[q[0]])
    dag.apply_operation_back(RZGate(-np.pi/2), qargs=[q[0]])
    dag.apply_operation_back(RZGate(-np.pi/2), qargs=[q[1]])

    dag.apply_operation_back(iSwapGate(), qargs=[q[0], q[1]])
    dag.apply_operation_back(CZGate(), qargs=[q[0], q[1]])
    dag.compose(get_h_dag(), qubits=[q[1]])
    #dag.apply_operation_back(HGate(), qargs=[q[1]])

    return dag

def translate_circuit(circuit):

    dag = circuit_to_dag(circuit)

    for node in dag.gate_nodes():

        if node.name == 'rzz':
            theta = node.op.params[0]
            zz_dag = get_zz_dag(theta)
            dag.substitute_node_with_dag(node, zz_dag)

        if node.name == 'rx':
            theta = node.op.params[0]
            rx_dag = get_rx_dag(theta)
            dag.substitute_node_with_dag(node, rx_dag)

        if node.name == 'swap':
            swap_dag = get_swap_dag()
            dag.substitute_node_with_dag(node, swap_dag)
    
        if node.name == 'h':
            h_dag = get_h_dag()
            dag.substitute_node_with_dag(node, h_dag)

