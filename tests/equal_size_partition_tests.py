import os
import numpy as np
from equal_size_partition.decode_state import decode_state
from equal_size_partition.get_ising_model import get_ising_model
from equal_size_partition.get_circuit import get_circuit
from equal_size_partition.get_cost_function import get_cost_function
from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution
from expectation_value import expectation_value_depolarizing, expectation_value_no_noise
from get_chalmers_circuit import get_chalmers_circuit
from equal_size_partition.gen_equal_size_partition_data import decode_file

def get_objecvtive(S):

    (J, h, bound) = get_ising_model(S)
    cost_function = get_cost_function(J, h, S)

    def objective(x):
        # if instnace of ndarray
        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        qc = get_circuit(gammas, betas, J, h)
        cqc = get_chalmers_circuit(qc)

        (exp_val, z_best) = expectation_value_depolarizing(0.99, cqc,
                 cost_function, repetitions=10000)

        return exp_val
    return (objective, bound)


def run_all_tests():

    decoded_file = decode_file('example_data_q4_q20')
    #print(decoded_file.tolist())
    
    for i,(arr, sol) in enumerate(decoded_file):
        S = np.array(arr)
        print(S)
        (objective, bound) = get_objecvtive(S)
        bounds = [(0, np.pi / 4), (0, np.pi)]

        bruteforce(objective, bounds, max_evaluations=4000,
                   save_file=prefix+'bruteforce_q'+str(i + 4), plot=True)

def inital_tests():
    dataset = [np.array([1, 2, 4, 3])]


    for i, S in enumerate(dataset):
        (objective, bound) = get_objecvtive(S)

        bruteforce(objective, [bound, bound], max_evaluations=1000,
                   save_file=prefix+'bruteforce_'+str(i))

        differential_evolution_p(
            objective, bound, p=1, save_file=prefix+'differential_evolution_p1_' + str(i))
        differential_evolution_p(
            objective, bound, p=2, save_file=prefix+'differential_evolution_p2_' + str(i))
        differential_evolution_p(
            objective, bound, p=3, save_file=prefix+'differential_evolution_p3_' + str(i))
        differential_evolution_p(
            objective, bound, p=4, save_file=prefix+'differential_evolution_p4_' + str(i))

        shgo_p(objective, bound, p=1, save_file=prefix+'shgo_p1_' + str(i))
        shgo_p(objective, bound, p=2, save_file=prefix+'shgo_p2_' + str(i))
        shgo_p(objective, bound, p=3, save_file=prefix+'shgo_p3_' + str(i))
        shgo_p(objective, bound, p=4, save_file=prefix+'shgo_p4_' + str(i))

def shgo_p(objective, bound, p, save_file=None):
    return shgo(objective, [bound] * p * 2, save_file)


def differential_evolution_p(objective, bound, p, save_file=None):
    return differential_evolution(objective, [bound] * p * 2, save_file)

prefix = os.path.join('tests', 'data', 'equal_size_partition', '')
os.makedirs(prefix, exist_ok=True)

run_all_tests()
