import os
import numpy as np
import scipy.io
from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution
from exact_cover_pontus.exact_cover_pontus import get_circuit, cost_function
from expectation_value import expectation_value_depolarizing_job, expectation_value_no_noise_job, expectation_value_bitflip_job, expectation_value_phaseflip_job, expectation_value_phasedamp_job, expectation_value_ampdamp_job
from expectation_value import expectation_value, probability_cost_distribution
from get_chalmers_circuit import get_chalmers_circuit


def get_no_noise_objective():
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas)
        cqc = get_chalmers_circuit(circuit)

        job = expectation_value_no_noise_job(cqc, repetitions=10000)
        (exp_val, z_best) = expectation_value(job, cost_function)

        return exp_val

    return objective


def get_depolarizing_objective(prob=0.99):
    def objective(x):

        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        circuit = get_circuit(gammas, betas)
        cqc = get_chalmers_circuit(circuit)

        job = expectation_value_depolarizing_job(prob, cqc, repetitions=10000)
        (exp_val, z_best) = expectation_value(job, cost_function)

        return exp_val

    return objective


def run_all_tests():

    #(gamma, beta) = run_no_noise_tests()
    (gamma, beta) = (0.9258, 2.7207)
    run_depoalrizing_noise_tests(gamma, beta)
    run_bitflip_noise_tests(gamma, beta)
    run_phaseflip_noise_tests(gamma, beta)
    run_ampdamp_noise_tests(gamma, beta)
    run_phasedamp_noise_tests(gamma, beta)


def run_depoalrizing_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'depo', '')

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        cqc = get_chalmers_circuit(circuit)
        job = expectation_value_depolarizing_job(
            fidelity, cqc, repetitions=10000)
        (dist, mean) = probability_cost_distribution(job, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'depo_f' + str(fidelity) + '.mat', v)

    print('depotest done')


def run_bitflip_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'bitflip', '')

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        cqc = get_chalmers_circuit(circuit)
        job = expectation_value_bitflip_job(fidelity, cqc, repetitions=10000)
        (dist, mean) = probability_cost_distribution(job, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'bitflip_f' + str(fidelity) + '.mat', v)

    print('bitflip test done')


def run_phaseflip_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'phaseflip', '')

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        cqc = get_chalmers_circuit(circuit)
        job = expectation_value_phaseflip_job(fidelity, cqc, repetitions=10000)
        (dist, mean) = probability_cost_distribution(job, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'phaseflip_f' + str(fidelity) + '.mat', v)

    print('phaseflip test done')


def run_ampdamp_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'ampdamp', '')

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        cqc = get_chalmers_circuit(circuit)
        job = expectation_value_ampdamp_job(fidelity, cqc, repetitions=10000)
        (dist, mean) = probability_cost_distribution(job, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'ampdamp_f' + str(fidelity) + '.mat', v)

    print('ampdamp test done')


def run_phasedamp_noise_tests(gamma, beta):
    prefix = os.path.join('tests', 'data', 'exact_cover', 'phasedamp', '')

    # fidelity has to be grater than about .15 becaus
    for fidelity in np.linspace(.5, 1, 20):
        if fidelity == 0:
            continue

        circuit = get_circuit(gamma, beta)
        cqc = get_chalmers_circuit(circuit)
        job = expectation_value_phasedamp_job(fidelity, cqc, repetitions=10000)
        (dist, mean) = probability_cost_distribution(job, cost_function)
        # Yeah, I know it's ugly.
        v = {'dist_keys': list(dist.keys()), 'dist_values': list(
            dist.values()), 'mean': mean, 'fidelity': fidelity}
        scipy.io.savemat(prefix + 'phasedamp_f' + str(fidelity) + '.mat', v)

    print('phase damp test done')


def run_no_noise_tests():
    prefix = os.path.join('tests', 'data', 'exact_cover', 'nonoise', '')
    os.makedirs(prefix, exist_ok=True)

    objective = get_no_noise_objective()
    bound = (0, np.pi)

    #run_bruteforce(objective, bound, prefix)
    #run_all_differential_evolution(objective, bound, 3, prefix)

    # Shgo won't complete for p=3, ran for 2h.
    #run_all_shgo(objective, bound, 3, prefix)

    result = run_single_differential_evolution(objective, bound, 1, prefix)
    print(result)
    return (result[0][0], result[0][1])


def run_bruteforce(objective, bound, prefix):
    bruteforce(objective, [bound, bound],
               save_file=prefix+'bruteforce', max_evaluations=2000, plot=False)


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


run_all_tests()
