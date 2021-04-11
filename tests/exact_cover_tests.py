import os
import numpy as np
import scipy.io
from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution
from exact_cover_pontus.exact_cover_pontus import get_circuit, cost_function

from expectation_value import expectation_value_depolarizing, expectation_value_no_noise, expectation_value_bitflip, expectation_value_phaseflip, expectation_value_phasedamp, expectation_value_ampdamp, expectation_value_amp_phase_damp
from expectation_value import expectation_value, probability_cost_distribution, approximation_ratio


def get_no_noise_objective():
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas)

        count_results = expectation_value_no_noise(circuit, repetitions=10000)
        (exp_val, z_best, r) = expectation_value(count_results, cost_function)

        print('Approximation ratio, no noise: ', r)

        return exp_val

    return objective


def get_depolarizing_objective(prob=0.99):
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas)

        count_results = expectation_value_depolarizing(prob, circuit, repetitions=10000)
        (exp_val, z_best, r) = expectation_value(count_results, cost_function)

        return exp_val

    return objective


def get_phase_damp_objective():
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas)

        count_results = expectation_value_phasedamp(0, circuit, repetitions=10000)
        (exp_val, z_best, r) = expectation_value(count_results, cost_function)

        print('Approximation ratio, phase damp: ', r)

        return exp_val

    return objective


def get_amp_damp_objective():
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas)

        count_results = expectation_value_ampdamp(0, circuit, repetitions=10000)
        (exp_val, z_best, r) = expectation_value(count_results, cost_function)

        r = approximation_ratio(exp_val, cost_best, cost_max)
        print('Approximation ratio, amplitude damp: ', r)

        return exp_val

    return objective


def get_amp_phase_damp_objective():
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas)

        count_results = expectation_value_amp_phase_damp(circuit, repetitions=10000)

        (exp_val, z_best, r) = expectation_value(count_results, cost_function)

        print('Approximation ratio, amplitude damp and phase damp: ', r)

        return exp_val

    return objective


def run_probability_test():
    # run_no_noise_tests()
    # run_phase_damp_probability_test()
    # run_amp_amp_probability_test()
    run_phase_amp_damp_probability_test()


def run_all_tests():

    # (gamma, beta) = run_no_noise_tests()
    (gamma, beta) = (0.9258, 2.7207)
    run_depoalrizing_noise_tests(gamma, beta)
    run_bitflip_noise_tests(gamma, beta)
    run_phaseflip_noise_tests(gamma, beta)
    run_ampdamp_noise_tests(gamma, beta)
    run_phasedamp_noise_tests(gamma, beta)


def run_depoalrizing_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'depo', '')
    os.makedirs(prefix, exist_ok=True)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        count_results = expectation_value_depolarizing(
            fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'depo_f' + str(fidelity) + '.mat', v)

    print('depotest done')


def run_bitflip_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'bitflip', '')
    os.makedirs(prefix, exist_ok=True)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        count_results = expectation_value_bitflip(fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'bitflip_f' + str(fidelity) + '.mat', v)

    print('bitflip test done')


def run_phaseflip_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'phaseflip', '')
    os.makedirs(prefix, exist_ok=True)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        count_results = expectation_value_phaseflip(fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'phaseflip_f' + str(fidelity) + '.mat', v)

    print('phaseflip test done')


def run_ampdamp_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'ampdamp', '')
    os.makedirs(prefix, exist_ok=True)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        count_results = expectation_value_ampdamp(fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'ampdamp_f' + str(fidelity) + '.mat', v)

    print('ampdamp test done')


def run_phasedamp_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'phasedamp', '')
    os.makedirs(prefix, exist_ok=True)

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        count_results = expectation_value_phasedamp(fidelity, circuit, repetitions=10000)
        (dist, mean) = probability_cost_distribution(count_results, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'phasedamp_f' + str(fidelity) + '.mat', v)

    print('phase damp test done')


def run_phase_damp_probability_test():
    prefix = os.path.join('tests', 'data', 'exact_cover',
                          'phasedamp_probability', '')
    os.makedirs(prefix, exist_ok=True)

    objective = get_phase_damp_objective()
    bound = (0, np.pi)

    run_bruteforce(objective, bound, prefix)

    print('phase damp porbability test done')


def run_phase_amp_damp_probability_test():
    prefix = os.path.join('tests', 'data', 'exact_cover',
                          'amp_phase_damp_probability', '')
    os.makedirs(prefix, exist_ok=True)

    objective = get_amp_phase_damp_objective()
    bound = (0, np.pi)

    run_bruteforce(objective, bound, prefix)

    print('phase amp damp probability test done')


def run_amp_amp_probability_test():
    prefix = os.path.join('tests', 'data', 'exact_cover',
                          'ampdamp_probability', '')
    os.makedirs(prefix, exist_ok=True)

    objective = get_amp_damp_objective()
    bound = (0, np.pi)

    run_bruteforce(objective, bound, prefix)

    print('amplitude damp probability test done')


def run_no_noise_tests():
    prefix = os.path.join('tests', 'data', 'exact_cover', 'nonoise', '')
    os.makedirs(prefix, exist_ok=True)

    objective = get_no_noise_objective()
    bound = (0, np.pi)

    run_bruteforce(objective, bound, prefix)

    # run_all_differential_evolution(objective, bound, 3, prefix)

    # Shgo won't complete for p=3, ran for 2h.
    # run_all_shgo(objective, bound, 3, prefix)

    # result = run_single_differential_evolution(objective, bound, 1, prefix)
    # print(result)
    # return (result[0][0], result[0][1])


def run_bruteforce(objective, bound, prefix):
    bruteforce(objective, [bound, bound],
               save_file=prefix+'bruteforce_ny', max_evaluations=2000, plot=False)


def run_single_shgo(objective, bound, p, prefix):
    return shgo_p(objective, bound, p, save_file=prefix+'shgo_p' + str(p))


def run_single_differential_evolution(objective, bound, p, prefix):
    return differential_evolution_p(objective, bound, p,
                                    save_file=prefix+'differential_evolution_p'+str(p))


def run_all_shgo(objective, bound, p, prefix):
    for i in range(1, p+1):
        run_single_shgo(objective, bound, i, prefix)


def run_all_differential_evolution(objective, bound, p, prefix):
    for i in range(1, p+1):
        run_single_differential_evolution(objective, bound, i, prefix)


def shgo_p(objective, bound, p, save_file=None):
    return shgo(objective, [bound] * p * 2, save_file)


def differential_evolution_p(objective, bound, p, save_file=None):
    return differential_evolution(objective, [bound] * p * 2, save_file)


run_probability_test()
