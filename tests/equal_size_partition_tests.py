import os
import numpy as np
import scipy.io

from equal_size_partition.decode_state import decode_state
from equal_size_partition.get_ising_model import get_ising_model

from get_circuit import get_circuit
from get_cost_function import get_cost_function

from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution

from expectation_value import expectation_value_depolarizing, expectation_value_no_noise, expectation_value_bitflip, expectation_value_phaseflip, expectation_value_phasedamp, expectation_value_ampdamp
from expectation_value import expectation_value, probability_cost_distribution
from equal_size_partition.gen_equal_size_partition_data import decode_file


def get_objective(S):

    (J, h, bound) = get_ising_model(S)
    cost_function = get_cost_function(J, h)

    def objective(x):
        # if instnace of ndarray
        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        qc = get_circuit(gammas, betas, J, h)

        count_results = expectation_value_depolarizing(0.99, qc, repetitions=10000)
        (exp_val, z_best, r) = expectation_value(count_results, cost_function)

        return exp_val
    return (objective, bound)


def get_no_noise_objective(S):

    (J, h, bound) = get_ising_model(S)
    cost_function = get_cost_function(J, h)

    def objective(x):

        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas, J, h)

        count_results = expectation_value_no_noise(circuit, repetitions=10000)
        (exp_val, z_best, r) = expectation_value(count_results, cost_function)

        return exp_val

    return (objective, bound)


def run_all_tests():

    decoded_file = decode_file('example_data_q4_q20')
    # print(decoded_file.tolist())

    for i, (arr, sol) in enumerate(decoded_file):
        S = np.array(arr)
        print(S)
        (objective, bound) = get_objective(S)
        bounds = [(0, np.pi / 4), (0, np.pi)]

        bruteforce(objective, bounds, max_evaluations=4000,
                   save_file=prefix+'bruteforce_q'+str(i + 4))


def run_all_tests_comparison():

    decoded_file = decode_file('example_data_q4_q20')
    # print(decoded_file.tolist())

    for i, (arr, sol) in enumerate(decoded_file):
        S = np.array(arr)
        print(S)
        (gamma, beta) = run_no_noise_tests(S)
        #(gamma, beta) = (0.9675, 2.7562)
        run_depoalrizing_noise_tests(gamma, beta, S)
        run_bitflip_noise_tests(gamma, beta, S)
        run_phaseflip_noise_tests(gamma, beta, S)
        run_ampdamp_noise_tests(gamma, beta, S)
        run_phasedamp_noise_tests(gamma, beta, S)


def run_no_noise_tests(S):
    prefix = os.path.join(
        'tests', 'data', 'equal_size_partition', 'nonoise', str(S),  '')
    os.makedirs(prefix, exist_ok=True)
    (objective, bound) = get_no_noise_objective(S)
    bounds = [(0, np.pi / 4), (0, np.pi)]

    # run_bruteforce(objective, bound, prefix)
    # run_all_differential_evolution(objective, bound, 3, prefix)

    # Shgo won't complete for p=3, ran for 2h.
    # run_all_shgo(objective, bound, 3, prefix)

    result = run_single_differential_evolution(objective, bound, 1, prefix)
    print(result)
    return (result[0][0], result[0][1])


def run_depoalrizing_noise_tests(gamma, beta, S):
    prefix = os.path.join(
        'tests', 'data', 'equal_size_partition', 'depo', str(S), '')
    os.makedirs(prefix, exist_ok=True)

    (J, h, bound) = get_ising_model(S)
    cost_function = get_cost_function(J, h)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta, J, h)
        count_results = expectation_value_depolarizing(
            fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'depo_f' + str(fidelity) + '.mat', v)

    print('depotest done')


def run_bitflip_noise_tests(gamma, beta, S):
    prefix = os.path.join(
        'tests', 'data', 'equal_size_partition', 'bitflip', str(S), '')
    os.makedirs(prefix, exist_ok=True)

    (J, h, bound) = get_ising_model(S)
    cost_function = get_cost_function(J, h)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta, J, h)
        count_results = expectation_value_bitflip(fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'bitflip_f' + str(fidelity) + '.mat', v)

    print('bitflip test done')


def run_phaseflip_noise_tests(gamma, beta, S):
    prefix = os.path.join(
        'tests', 'data', 'equal_size_partition', 'phaseflip', str(S), '')
    os.makedirs(prefix, exist_ok=True)

    (J, h, bound) = get_ising_model(S)
    cost_function = get_cost_function(J, h)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta, J, h)
        count_results = expectation_value_phaseflip(fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'phaseflip_f' + str(fidelity) + '.mat', v)

    print('phaseflip test done')


def run_ampdamp_noise_tests(gamma, beta, S):
    prefix = os.path.join(
        'tests', 'data', 'equal_size_partition', 'ampdamp', str(S), '')
    os.makedirs(prefix, exist_ok=True)

    (J, h, bound) = get_ising_model(S)
    cost_function = get_cost_function(J, h)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta, J, h)
        count_results = expectation_value_ampdamp(fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'ampdamp_f' + str(fidelity) + '.mat', v)

    print('ampdamp test done')


def run_phasedamp_noise_tests(gamma, beta, S):
    prefix = os.path.join(
        'tests', 'data', 'equal_size_partition', 'phasedamp', str(S), '')
    os.makedirs(prefix, exist_ok=True)

    (J, h, bound) = get_ising_model(S)
    cost_function = get_cost_function(J, h)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta, J, h)
        count_results = expectation_value_phasedamp(fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'phasedamp_f' + str(fidelity) + '.mat', v)

    print('phase damp test done')


def inital_tests():
    dataset = [np.array([1, 2, 4, 3])]

    for i, S in enumerate(dataset):
        (objective, bound) = get_objective(S)

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


def run_single_differential_evolution(objective, bound, p, prefix):
    return differential_evolution_p(objective, bound, p,
                                    save_file=prefix+'differential_evolution_p'+str(p))


prefix = os.path.join('tests', 'data', 'equal_size_partition', '')
os.makedirs(prefix, exist_ok=True)

run_all_tests_comparison()
