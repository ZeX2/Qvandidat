import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.dagcircuit import DAGCircuit
from qiskit.transpiler import PassManager
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.circuit.library import RYGate, RZGate, CXGate, CZGate,\
        HGate, iSwapGate, RXGate, RZZGate, SwapGate, U2Gate
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary as sel
from qiskit.transpiler.passes import BasisTranslator, Unroller 
from qiskit.circuit import EquivalenceLibrary, Parameter, QuantumRegister

def change_bases(circuit, bases):
    pass_ = Unroller(bases)
    pm = PassManager(pass_)
    new_circuit = pm.run(circuit)
    return new_circuit


# The main goal is to translate QAOA circuits, this may or may not work
# as expected with gates not used in QAOA circuits
def translate_circuit2(circuit):

    # The first step is to translate to some known simple gates
    basis_gates = ['swap', 'cz', 'H', 'barrier', 'u3', 'rzz', 'measure']
    bt_pass = BasisTranslator(sel, basis_gates)
    
    dag_simple = bt_pass.run(circuit_to_dag(circuit))
    print('')
    print('')
    print('')
    print('')
    print('')
    print('DAG SIMPLE')
    print(dag_to_circuit(dag_simple))
    
    # Now we only have to translate from basis_gates to chalmers gates
    # We calculate those by hand because
    basis_gates_chalmers = ['iswap', 'cz', 'barrier', 'u3', 'measure']
    chalmers_sel = EquivalenceLibrary()
    
    theta_rx = Parameter('theta')
    theta_rzz = Parameter('theta')


    chalmers_sel.add_equivalence(RXGate(theta_rx), get_rx_circuit(theta_rx))
    chalmers_sel.add_equivalence(RZZGate(theta_rzz), get_zz_circuit(theta_rzz))
    chalmers_sel.add_equivalence(HGate(), get_h_circuit())
    chalmers_sel.add_equivalence(SwapGate(), get_swap_circuit())

    bt_pass = BasisTranslator(chalmers_sel, basis_gates_chalmers)
    
    dag_chalmers = bt_pass.run(dag_simple)

    print('')
    print('')
    print('')
    print('')
    print('')
    print('DAG CHALMERS')
    print(dag_to_circuit(dag_chalmers))
    return dag_to_circuit(dag_chalmers)


# Should be eqvivalent to:
#circuit.ry(-np.pi/2)
#circuit.rz(angle)
#circuit.ry(np.pi/2)
def get_rx_circuit(angle):
    q = QuantumRegister(1, "q")
    circuit = QuantumCircuit(q)

    # Do chalmers allow -pi/2 or should it be np.pi/2 * 3?
    circuit.ry(-np.pi/2, q)
    circuit.rz(angle, q)
    circuit.ry(np.pi, q)
    
    #print(dag_to_circuit(dag))
    return circuit

def get_zz_circuit(angle):
    q = QuantumRegister(2, "q")
    circuit = QuantumCircuit(q)

    circuit.compose(get_h_circuit(), qubits=[q[1]], inplace=True)
    circuit.append(CZGate(), qargs=[q[0], q[1]])

    circuit.compose(get_rx_circuit(angle), qubits=[q[1]], inplace=True)

    circuit.append(CZGate(), qargs=[q[0], q[1]])
    circuit.compose(get_h_circuit(), qubits=[q[1]], inplace=True)

    return circuit

def get_h_circuit():
    q = QuantumRegister(1, "q")
    circuit = QuantumCircuit(q)

    circuit.append(RZGate(np.pi), qargs=q)
    circuit.append(RYGate(np.pi/2), qargs=q)
    
    return circuit

def get_swap_circuit():
    q = QuantumRegister(2, "q")
    circuit = QuantumCircuit(q)

    circuit.compose(get_h_circuit(), qubits=[q[0]], inplace=True)

    circuit.append(RZGate(-np.pi/2), qargs=[q[0]])
    circuit.append(RZGate(-np.pi/2), qargs=[q[1]])

    circuit.append(iSwapGate(), qargs=[q[0], q[1]])

    circuit.append(CZGate(), qargs=[q[0], q[1]])
    circuit.compose(get_h_circuit(), qubits=[q[0]], inplace=True)

    return circuit

def translate_circuit(circuit):

    dag = circuit_to_dag(circuit)

    for node in dag.gate_nodes():

        if node.name == 'rzz':
            theta = node.op.params[0]
            zz_dag = circuit_to_dag(get_zz_circuit(theta))
            dag.substitute_node_with_dag(node, zz_dag)

        if node.name == 'rx':
            theta = node.op.params[0]
            rx_dag = circuit_to_dag(get_rx_circuit(theta))
            dag.substitute_node_with_dag(node, rx_dag)

        if node.name == 'swap':
            swap_dag = circuit_to_dag(get_swap_circuit())
            dag.substitute_node_with_dag(node, swap_dag)
    
        if node.name == 'h':
            h_dag = circuit_to_dag(get_h_circuit())
            dag.substitute_node_with_dag(node, h_dag)

    return dag_to_circuit(dag)
