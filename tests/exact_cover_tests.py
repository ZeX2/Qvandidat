import os
import numpy as np
from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution
from exact_cover_pontus.exact_cover_pontus import get_circuit, cost_function
from expectation_value import expectation_value_depolarizing, expectation_value_no_noise
from get_chalmers_circuit import get_chalmers_circuit


def get_objective():
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas)
        cqc = get_chalmers_circuit(circuit)
        
        (exp_val, z_best) = expectation_value_depolarizing(0.99,
                cqc, cost_function, repetitions=10000)

        return exp_val

    return objective


def run_all_tests():
    prefix = os.path.join('tests', 'data', 'exact_cover', '')
    os.makedirs(prefix, exist_ok=True)

    objective = get_objective()
    bound = (0, np.pi)

    r = bruteforce(objective, [bound, bound],
                   save_file=prefix+'bruteforce'
                   max_evaluations=2000, plot=False)


    differential_evolution_p(
        objective, bound, p=1, save_file=prefix+'differential_evolution_p1')
    differential_evolution_p(
        objective, bound, p=2, save_file=prefix+'differential_evolution_p2')
    differential_evolution_p(
        objective, bound, p=3, save_file=prefix+'differential_evolution_p3')
    differential_evolution_p(
        objective, bound, p=4, save_file=prefix+'differential_evolution_p4')

    shgo_p(objective, bound, p=1, save_file=prefix+'shgo_p1')
    shgo_p(objective, bound, p=2, save_file=prefix+'shgo_p2')
    shgo_p(objective, bound, p=3, save_file=prefix+'shgo_p3')
    shgo_p(objective, bound, p=4, save_file=prefix+'shgo_p4')

def shgo_p(objective, bound, p, save_file=None):
    return shgo(objective, [bound] * p * 2, save_file)


def differential_evolution_p(objective, bound, p, save_file=None):
    return differential_evolution(objective, [bound] * p * 2, save_file)


run_all_tests()
