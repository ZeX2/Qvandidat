import os
import time
import numpy as np

from problem_group.integer_bin_packing import integer_bin_packing as get_ising_model
from problem_group.integer_bin_packing import correct_solution as is_valid_solution, decode_integer_bin_packing as decode_solution

from problem_group.integer_bin_packing_data_generator import decode_file

from classical_optimizers.global_search_algorithms import bruteforce

from get_circuit import get_circuit
from get_cost_function import get_cost_function
from expectation_value import expectation_value, expectation_value_no_noise_state_vector

from utils import save_results


def get_no_noise_objective(S):

    (J, h, const, A, B, C) = get_ising_model(**S)
    cost_function = get_cost_function(J, h, const)

    def objective(x):

        p = int(len(x)/2)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas, J, h, measure=False)

        count_results = expectation_value_no_noise_state_vector(circuit)
        (exp_val, z_best, r) = expectation_value(count_results, cost_function)

        return exp_val

    return objective


def run_bruteforce(S):
    prefix = get_bin_packing_prefix('nonoise_sv')

    objective = get_no_noise_objective(S)
    bound = [(0, 2 * np.pi/2), (0, np.pi/2)]

    start_time = time.monotonic()
    results = bruteforce(objective, bound, max_evaluations=4000)
    end_time = time.monotonic()
    
    
    full_filename = prefix + str(S) + '_bruteforce'
    save_results(results, S, end_time-start_time, full_filename, results[2])


def get_bin_packing_prefix(category):
    prefix = os.path.join('tests', 'data', 'bin_packing',
                          category, '')
    os.makedirs(prefix, exist_ok=True)
    return prefix


def generate_energy_landscapes():
    data_dirr = os.path.join('problem_group', 'data')

    visited_problems = set()
    problems = []
    num_of_problems = np.zeros((31, 3), dtype=int)

    for root, _, files in os.walk(data_dirr, topdown=False):
        num_qubits = list(map(int, map(lambda x: x.split('_n')[1], files)))
        #order = np.argsort(num_qubits)[::-1] # also reverse to do hard problems first
        order = np.argsort(num_qubits)
        np_files = np.array(files)
        for filename in np_files[order]:
            for S in decode_file(filename):
                if str(S) in visited_problems: continue

                I = len(S['W'])
                W_max = S['W_max']
                n = I*I + I*W_max
                num_of_problems[n, 1] += 1
                num_of_problems[n, 0] = n

                #if I*I + I*W_max > 10: continue
                #if I < 2: continue

                visited_problems.add(str(S))
                problems.append((S)

    for i in range(len(num_of_problems)):
        num_of_problems[i, 2] = num_of_problems[i, 1]
        if i > 0: num_of_problems[i, 2] += num_of_problems[i-1, 2]

    print('Number of problems to solve:', len(problems))
    print(num_of_problems)
    print('Starting bruteforce')

    i = 0
    for S in problems:
        i += 1
        print(str(S), i, '/', num_of_problems[-1, 2])
        run_bruteforce(S)


    #print(np.cumsum(num_of_problems, dtype=int))

generate_energy_landscapes()
