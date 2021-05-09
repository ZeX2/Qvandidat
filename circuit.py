from funcs import *
from integer_bin_packing import *
from main import *

from problem_list_circuit import get_problem_list
from qiskit.visualization import circuit_drawer


def main(problem_number):
    print(problem_number)

    # prioritized order
    problem_list = get_problem_list()
    problem_dict = problem_list[problem_number]
    
    _calculate_circuit_stats(**problem_dict)

def _calculate_circuit_stats(W,W_max,p):

    J, h, const, A, B, C = integer_bin_packing(W, W_max)
    gamma = np.sqrt(2) / np.pi
    beta = (1 + np.sqrt(5)) / np.sqrt(2)

    S = {'W':W, 'W_max':W_max,'A':A, 'B':B, 'C':C}
    
    I = len(W)
    n = I * I + I * W_max

    print(S)
    lin_circ = linear_swap_chalmers_circuit(gamma, beta, J, h)
    print('Linear swap:')
    print('Operations ', lin_circ.count_ops())
    print('Depth ', lin_circ.depth())
    print()

    ling_circ = linear_swap_grid_chalmers_circuit(gamma, beta, J, h)
    print('Linear swap grid:')
    print('Operations ', ling_circ.count_ops())
    print('Depth ', ling_circ.depth())
    print()

    if n in [2**k for k in range(0, 10)]:
        print('Swap network:')
        net_circ = swap_network_chalmers_circuit(gamma, beta, J, h)
        net_circ2 = swap_network_chalmers_circuit2(gamma, beta, J, h)
        print('Operations ', net_circ.count_ops())
        print('Depth ', net_circ.depth())
        print()
        if n == 4:
            circ = qaoa_ising_circuit(J, h, gamma, beta)
            print(circ)
            print(net_circ2)
            print(net_circ)
            #circuit_drawer(net_circ2, output='latex_source', filename=str(n)+'four_qubit_after.png')
            #circuit_drawer(circ, output='latex_source', filename=str(n)+'four_qubit_before.png')

    if n < 6:
        print('Star swap:')
        star_circ = star_swap_chalmers_circuit(gamma, beta, J, h)
        print('Operations ', star_circ.count_ops())
        print('Depth ', star_circ.depth())
        print()

    trans_circ = transpile_swap_chalmers_circuit(gamma, beta, J, h)
    print('Transpile swap (Qiskit):')
    print('Operations ', trans_circ.count_ops())
    print('Depth ', trans_circ.depth())
    print()
    

 
if __name__ == '__main__':

    #main(int(sys.argv[1]))
    for i in range(0, 3):
        main(i)

