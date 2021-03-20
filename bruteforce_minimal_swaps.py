import numpy as np
import itertools

pp = 0

# Diamond chalmers n=5
def get_qubit_map_chalmers_diamond():
    n = 5
    qubit_map_vec = []

    qubit_map_vec.append((0, 1))
    qubit_map_vec.append((2, 1))
    qubit_map_vec.append((3, 1))
    qubit_map_vec.append((4, 1))

    return (n, qubit_map_vec)

def get_qubit_map_test_n6():
    n = 6
    qubit_map_vec = []

    qubit_map_vec.append((0, 1))
    qubit_map_vec.append((2, 1))
    qubit_map_vec.append((3, 1))
    qubit_map_vec.append((4, 1))
    qubit_map_vec.append((5, 1))

    return (n, qubit_map_vec)

def get_qubit_map_grid(r = 4, c = 5):
    n = r * c
    qubit_map_vec = []

    for i in range(r):
        for j in range(c-1):
            qubit_map_vec.append((j + i*c, j+1 + i*c))

    for j in range(c):
        for i in range(r-1):
            qubit_map_vec.append((j + i*c, j + (i+1)*c))

    return (n, qubit_map_vec)

#(n, qubit_map_vec) = get_qubit_map_chalmers_diamond()
#Solution found with pairs  [(0, 1), (1, 2), (1, 3)]

#(n, qubit_map_vec) = get_qubit_map_grid(3, 3)
#Solution found with pairs  [(0, 5), (0, 8), (1, 6), (1, 2), (3, 4), (2, 7)]
# Took nearly 10h on laptop

#(n, qubit_map_vec) = get_qubit_map_test_n6()
#Solution found with pairs  [(0, 1), (1, 2), (1, 3), (1, 4)]

#(n, qubit_map_vec) = get_qubit_map_grid()
#no solution after hours.

operations = np.tril(np.random.rand(n,n) * 100, -1)

least_operations = n*n

def test_operations(pairs):
    global least_operations

    ops = np.copy(operations)
    qubits = list(range(n))

    for pair in pairs:
        p1, p2 = pair
        qubits[p1], qubits[p2] = qubits[p2], qubits[p1]
        do_allowed_operations(qubits, ops)

        if np.count_nonzero(ops != 0) < least_operations:
            least_operations = np.count_nonzero(ops != 0)
            #print(least_operations)

            if np.all((ops == 0)): return True

    return False

def do_allowed_operations(qubits, operations):

    for allowed_interaction in qubit_map_vec:
        q1, q2 = allowed_interaction
        qq1, qq2 = qubits[q1], qubits[q2]

        operations[max(qq1,qq2), min(qq1,qq2)] = 0

def recurse(current_depth: int, current_pairs: [], depth: int):

    if current_depth == depth:
        global pp
        pp = pp + 1
        if pp%10000 == 0: print(current_pairs, least_operations)

        if test_operations(current_pairs):
            print('Solution found with pairs ', current_pairs)
            exit(0)
        return
    
    for i in range(n):
        for j in range(i+1,n):
            recurse(current_depth + 1, current_pairs + [(i,j)], depth)

do_allowed_operations(list(range(n)), operations)

for i in itertools.count(1):
    recurse(0, [], i)

