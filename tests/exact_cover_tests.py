import numpy as np
from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution
from exact_cover_pontus.expectation_value_qiskit import expectation_value as expectation_value_exact_cover


def get_objective():
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gamma = x[0]
        beta = x[1]

        exp_val = expectation_value_exact_cover(gamma,
                beta, repetitions=1000)

        return exp_val

    return objective()


def run_all_tests():
    objective = get_objective()

    r = bruteforce(objective, [(0, np.pi/2), (0, np.pi/2)],
               max_evaluations=10000, plot=True)



