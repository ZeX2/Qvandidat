from qiskit import QuantumCircuit
import numpy as np
import matplotlib
from swap_network import *
from compare_routing_techniques import *
from linear_swap import *

def decomposing_circuit():
    circuit = QuantumCircuit(7)
    circuit.h(3)
    circuit.swap(2,3)
    circuit.h(4)
    circuit.cx(1,6)
    circuit.cx(2,5)
    circuit.cx(4,5)
    circuit.cx(6,1)
    print(circuit.draw())
    circuit.decompose()
    print(circuit.decompose().draw())

def UR_and_UL_for_array():
    List = [1, 2, 3, 4, 5, 6] 
    print(List)
    N = len(List)
    for i in range(0,int(N/2),1):
        UL_swap(List)
        print(List)
        UR_swap(List)
        print(List)

#UR_and_UL_for_array()

def test_swap_pos():
    List = [1, 2, 3, 4, 5, 6]
    swap_all_pos(List)
    print(List)

def test_swap_pos_shifted():
    List = [1, 2, 3, 4, 5, 6]
    print(List)
    N = len(List)
    for i in range(0,N-1,2):
        List = swapPositions(List, i, i+1)
        print(List)


#test_swap_pos_shifted()


def color_swap_array():
    N2 = 32
    newarray = []
    for i in range(N2):
        if i%2 == 1:
            newarray.append(2)
        else:
            newarray.append(1)
    print(newarray)
    print(swap_all_pos(newarray))

    array = np.array(range(0,32,1)).reshape(4,8)
    print(array)

    print(color_sep(array))


def test_swap_network():
    S = np.array([1, 2, 3, 4])
    B = 1
    A = B*max(S)^2 + 1
    gamma = 1.3
    beta = 2.7

    J = A+B*S.reshape(-1,1)*S
    circuit = swap_network(J, gamma, beta)
    circuit.draw(output='mpl', filename='Fully_working_SN')
#test_swap_network()

def test_routing():
    S = np.array([1, 2, 3, 4])
    B = 1
    A = B*max(S)^2 + 1
    gamma = 1.3
    beta = 2.7

    J = A+B*S.reshape(-1,1)*S
    coupling =  [[0,1], [0,2], [1,3], [2,3]]
    compare_circuit_depth(J, gamma, beta, coupling)

#test_routing()

def test_grid_to_path():
    grid = np.array(range(0,16,1)).reshape(4,4)
    print(grid)
    print(qubit_path(grid))

def test_seperate_grid():
    grid = np.array(range(0,16,1)).reshape(4,4)
    print(grid)
    print(seperate_grid(grid))


def test_grids():
    qubit_grid = np.array(range(8)).reshape(2,4)
    print(qubit_grid)
    circuit = QuantumCircuit(8)

    qc_color_sep(circuit, qubit_grid)
    print(qubit_grid)
    print(seperate_grid(qubit_grid))

def test_get_logical_grid():
    n = 8

    q_grid = get_qubit_grid(n)
    print(q_grid)
    q_path = get_qubit_path(q_grid)
    print(q_path)

    l_grid = get_logical_grid(q_path, q_grid)
    print(l_grid)
    
def test_linear_routing():
    S = np.array([1, 2, 3, 4])
    B = 1
    A = B*max(S)^2 + 1
    gamma = 1.3
    beta = 2.7

    J = A+B*S.reshape(-1,1)*S
    circuit = linear_swap_method(J, gamma, beta)
    circuit.draw(output='mpl', filename='SWAP_ladder')
#test_swap_network()
test_linear_routing()