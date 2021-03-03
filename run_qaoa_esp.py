import numpy as np
from equal_size_partition.decode_state import decode_state
from equal_size_partition.get_ising_model import get_ising_model
from equal_size_partition.get_circuit import get_circuit
from equal_size_partition.get_cost_function import get_cost_function
from equal_size_partition.get_chalmers_circuit import get_chalmers_circuit
from equal_size_partition.get_expectation_value import expectation_value
from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution
from exact_cover_pontus.expectation_value_qiskit import expectation_value as expectation_value_exact_cover


S = np.array([1, 2, 4, 3])
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

    (exp_val, z_best) = expectation_value(
        cqc, cost_function, repetitions=1000)
    return exp_val


def objective_exact_cover(x):

    p = int(len(x)/2)
    print(x)

    gamma = x[0]
    beta = x[1]

    exp_val = expectation_value_exact_cover(gamma, beta, repetitions=1000)
    return exp_val


def decode_solution(x):

    p = int(len(x)/2)

    gammas = x[0:p]
    betas = x[p:2*p]

    qc = get_circuit(gammas, betas, J, h)
    cqc = get_chalmers_circuit(qc)

    (exp_val, z_best) = expectation_value(cqc, cost_function, repetitions=1000)
    return decode_state(z_best, S)


gamma_0 = np.array([.3, .4])
beta_0 = np.array([.7, .6])

x0 = np.concatenate([gamma_0, beta_0])

# r = differential_evolution(objective, [bound, bound])
r = bruteforce(objective, [(0, np.pi/2), (0, np.pi/2)],
               max_evaluations=1000, plot=False, save_file='hej')
# (a, b) = decode_solution(r[0])
# print(a, b, sum(a))

print('Things are working!')
