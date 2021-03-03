import numpy as np
from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution
from exact_cover_pontus.exact_cover_pontus import get_circuit, cost_function
from expectation_value import expectation_value_depolarizing, expectation_value_no_noise


def get_objective():
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gamma = x[0]
        beta = x[1]

        exp_val = expectation_value_depolarizing(repetitions=1000)

        return exp_val

    return objective


def run_all_tests():
    objective = get_objective()
    r = bruteforce(objective, [(0, np.pi/2), (0, np.pi/2)],
                   max_evaluations=10000, plot=True)


run_all_tests()
