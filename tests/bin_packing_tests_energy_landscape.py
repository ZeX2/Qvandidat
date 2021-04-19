import os
import numpy as np

from problem_group.integer_bin_packing import integer_bin_packing as get_ising_model
from problem_group.integer_bin_packing import correct_solution as is_valid_solution, decode_integer_bin_packing as decode_solution

from problem_group.integer_bin_packing_data_generator import decode_file

from classical_optimizers.global_search_algorithms import bruteforce

from get_circuit import get_circuit
from get_cost_function import get_cost_function
from expectation_value import expectation_value, expectation_value_no_noise_state_vector


def get_no_noise_objective(S):

    (J, h, const, A, B, C) = get_ising_model(**S, C_factor=3)
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


def run_bruteforce(S, filename):
    prefix = get_bin_packing_prefix('nonoise_sv', filename)

    objective = get_no_noise_objective(S)
    bound = [(0, 2 * np.pi), (0, np.pi)]

    bruteforce(objective, bound, max_evaluations=4000,
               save_file=prefix + str(S) + '_bruteforce')


def get_bin_packing_prefix(category, filename):
    prefix = os.path.join('tests', 'data', 'bin_packing',
                          category, filename, '')
    os.makedirs(prefix, exist_ok=True)
    return prefix


def generate_energy_landscapes():
    data_dirr = os.path.join('problem_group', 'data')

    for root, _, files in os.walk(data_dirr, topdown=False):
        num_qubits = list(map(int, map(lambda x: x.split('_n')[1], files)))
        order = np.argsort(num_qubits)
        np_files = np.array(files)
        for filename in np_files[order]:
            for S in decode_file(filename):
                print(str(S), filename)
                run_bruteforce(S, filename)


generate_energy_landscapes()
