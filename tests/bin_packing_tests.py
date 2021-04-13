import os
import numpy as np
import scipy.io

import time
from datetime import timedelta, datetime

from problem_group.integer_bin_packing import integer_bin_packing as get_ising_model
from problem_group.integer_bin_packing import correct_solution as is_valid_solution, decode_integer_bin_packing as decode_solution

from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution

from get_circuit import get_circuit
from get_cost_function import get_cost_function
from expectation_value import expectation_value_depolarizing, expectation_value_no_noise, expectation_value_bitflip, expectation_value_phaseflip, expectation_value_phasedamp, expectation_value_ampdamp
from expectation_value import expectation_value, probability_cost_distribution, expectation_value_no_noise_state_vector


def get_no_noise_objective(S):

    (J, h, const) = get_ising_model(**S)
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


def run_brutforce_test(S):
    prefix = get_bin_packing_prefix('nonoise', str(S))

    (objective, bound) = get_no_noise_objective(S)
    bound = [(0, 2* np.pi), (0, np.pi)]

    bruteforce(objective, bound, max_evaluations=4000,
                save_file=prefix+'bruteforce_q'+str(i + 4))


def run_no_noise_test(S):
    prefix = get_bin_packing_prefix('nonoise_sv', str(S))
    
    objective = get_no_noise_objective(S)

    #print(objective(np.array([6.19056936, 2.7129152])))
    #print('Bye')
    #exit(0)

    # gammas betas
    bound = [(0, 2 * np.pi), (0, np.pi)]

    for p in range(1, 13):
        start_time = time.monotonic()
        result = run_single_differential_evolution(objective, bound, p, prefix)
        print(result)
        end_time = time.monotonic()
        print('Time to find optimal angles:', timedelta(seconds=end_time - start_time),'Time now:', datetime.now(), 'Expected value:', objective(result[0]), 'p:', p, 'gammas', result[0][0:p], 'betas', result[0][p:p*2], str(S))
    
def shgo_p(objective, bound, p, save_file=None):
    return shgo(objective, [bound] * p * 2, save_file)


def differential_evolution_p(objective, bound, p, save_file=None):
    return differential_evolution(objective, np.tile(bound, (p, 1)), save_file)


def run_single_differential_evolution(objective, bound, p, prefix):
    return differential_evolution_p(objective, bound, p,
                                    save_file=prefix+'differential_evolution_p'+str(p))


def get_bin_packing_prefix(category, problem_str):
    prefix = os.path.join('tests', 'data', 'bin_packing', category,\
                          str(datetime.now()), problem_str,  '')
    os.makedirs(prefix, exist_ok=True)
    return prefix

S = {'W': [1, 1], 'W_max': 2, 'A': 2, 'B': 1}
run_no_noise_test(S)

