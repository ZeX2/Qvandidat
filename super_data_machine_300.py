import os
import json
from pathlib import Path

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.stats import sem

from integer_bin_packing import *
from funcs import *

def filter_data(data, conditions):
    return list(filter(lambda item: all(((k in item and item[k]==v)for (k,v) in conditions.items())), data))

def time_in_sec(time):
    h, m, s = [float(i) for i in time.split(':')]
    return int(3600*h + 60*m + s)

def problem_dict2str(problem):
    return f"W={problem['W']}-W_max={problem['W_max']}-A={problem['A']}-B={problem['B']}-C={problem['C']}"
    
dir_path = os.getcwd()
data_path = os.path.join(dir_path, 'results')
data_json_paths = [f for f in os.listdir(data_path) if f.endswith('.json.json')]

data = {}
for file_name in data_json_paths:
    with open(os.path.join(data_path, file_name)) as f:
        data[file_name.rstrip('.json.json')] = json.load(f)
        #data.append(json.load(f))

unique_problems = []
unique_instances = []
for problem_instance in data.values():
    problem = problem_instance['problem']
    unique_instances.append(problem)
    problem = {k: problem[k] for k in ['W', 'W_max']}
    unique_problems.append(problem)

unique_instances = set([str(i) for i in unique_instances])
unique_instances = [eval(i) for i in unique_instances]
unique_problems = set([str(i) for i in unique_problems])
unique_problems = [eval(i) for i in unique_problems]

#%% Data extraction
instances_data = {}
landscape_data = {}
noise = False #If noise or not
noise_string = 'noise' if noise else 'state'
conditions_ = {'noise': noise}
for instance in unique_instances:
    conditions = {'problem': instance, **conditions_}
    instances_data[str(instance)] = filter_data(data.values(), conditions)
    landscape_data[str(instance)] = next((d for d in data.values() if 'landscape' in d and d['problem']==instance), None)

exp_data = {}
approx_ratio_data = {}
optimal_prob_data = {}
valid_prob_data = {}
avg_time_data = {}

for problem, instances in instances_data.items():
    if not instances:
        continue
    J, h, const, A, B, C = integer_bin_packing(**eval(problem))
    TrJ = np.trace(J)
    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, TrJ)/B for bits in bits_list}
    min_cost = min(costs.values())
    max_valid_cost = len(eval(problem)['W'])
    
    p_values = sorted(list({instance['p'] for instance in instances}))
    exp_costs = {'avg': [], 'best': [], 'std': []}
    approx_ratios = {'avg': [], 'best': [], 'std': []}
    optimal_probs = {'avg': [], 'best': [], 'std': []}
    valid_probs = {'avg': [], 'best': [], 'std': []}
    times = {'avg': [], 'best': [], 'std': []}

    for p in p_values:
        exp_cost = [instance['expected_value'] for instance in instances if instance['p']==p]
        exp_costs['avg'].append(np.mean(exp_cost))
        exp_costs['best'].append(min(exp_cost))
        exp_costs['std'].append(sem(exp_cost))

        approx_ratio = [instance['approximation_ratio'] for instance in instances if instance['p']==p]
        approx_ratios['avg'].append(np.mean(approx_ratio))
        approx_ratios['best'].append(max(approx_ratio))
        approx_ratios['std'].append(sem(approx_ratio))
        
        optimal_prob = [instance['probability_distribution'][str(min_cost)] for instance in instances
                        if (instance['p']==p and str(min_cost) in instance['probability_distribution'])]
        optimal_probs['avg'].append(np.mean(optimal_prob))
        optimal_probs['best'].append(max(optimal_prob))
        optimal_probs['std'].append(sem(optimal_prob))

        valid_prob = [sum(float(prob) for cost, prob in instance['probability_distribution'].items() 
                                   if float(cost) <= max_valid_cost)
                               for instance in instances if instance['p']==p]
        valid_probs['avg'].append(np.mean(valid_prob))
        valid_probs['best'].append(max(valid_prob))
        valid_probs['std'].append(sem(valid_prob))
        
        time = [time_in_sec(instance['execution_time']) for instance in instances if instance['p']==p]
        times['avg'].append(np.mean(time))

    exp_data[problem] = (p_values, exp_costs)
    approx_ratio_data[problem] = (p_values, approx_ratios)
    optimal_prob_data[problem] = (p_values, optimal_probs)
    valid_prob_data[problem] = (p_values, valid_probs)
    avg_time_data[problem] = (p_values, times)

#%% Plotting
err_bar_format = {'capsize': 5, 'elinewidth': 2, 'capthick': 2, 'barsabove': True}

plots = ['expected_cost', 'approximation_ratio', 'optimal_solution', 'valid_solution', 'execution_time', 'landscape']
for plot in plots:
    for sim_type in ['state', 'noise']:
        Path(f'plots/{plot}/{sim_type}').mkdir(parents=True, exist_ok=True)

show_plots = False

# Expected value vs p
for problem, plot_data in exp_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1]['best'], '-o', label='Lowest')
    plt.errorbar(plot_data[0], plot_data[1]['avg'], fmt='-o', yerr=plot_data[1]['std'], label='Average', **err_bar_format)
    plt.ylabel('Expected cost')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.legend()
    if show_plots: plt.show()
    problem_string = problem_dict2str(eval(problem))
    plt.savefig(f'plots/expected_cost/{noise_string}/expected_cost-{noise_string}-{problem_string}-')

# Approximation ratio vs p
for problem, plot_data in approx_ratio_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1]['best'], '-o', label='Highest')
    plt.errorbar(plot_data[0], plot_data[1]['avg'], fmt='-o', yerr=plot_data[1]['std'], label='Average', **err_bar_format)
    plt.ylabel('Approximation ratio')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.legend()
    if show_plots: plt.show()
    problem_string = problem_dict2str(eval(problem))
    plt.savefig(f'plots/approximation_ratio/{noise_string}/approximation_ratio-{noise_string}-{problem_string}')

# Probability of optimal solution vs p
for problem, plot_data in optimal_prob_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1]['best'], '-o', label='Highest')
    plt.errorbar(plot_data[0], plot_data[1]['avg'], fmt='-o', yerr=plot_data[1]['std'], label='Average', **err_bar_format)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.ylabel('Probability of optimal solution')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.show()
    plt.legend()
    if show_plots: plt.show()
    problem_string = problem_dict2str(eval(problem))
    plt.savefig(f'plots/optimal_solution/{noise_string}/optimal_solution-{noise_string}-{problem_string}')
    
# Probability of valid solution vs p
for problem, plot_data in valid_prob_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1]['best'], '-o', label='Highest')
    plt.errorbar(plot_data[0], plot_data[1]['avg'], fmt='-o', yerr=plot_data[1]['std'], label='Average', **err_bar_format)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.ylabel('Probability of valid solution')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.show()
    plt.legend()
    if show_plots: plt.show()
    problem_string = problem_dict2str(eval(problem))
    plt.savefig(f'plots/valid_solution/{noise_string}/valid_solution-{noise_string}-{problem_string}')

# Average execution time vs p
for problem, plot_data in avg_time_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1]['avg'], '-o')
    plt.ylabel('Average execution time (s)')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.show()
    if show_plots: plt.show()
    problem_string = problem_dict2str(eval(problem))
    plt.savefig(f'plots/execution_time/{noise_string}/execution_time-{noise_string}-{problem_string}')

# Energy landscapes
for problem, landscape in landscape_data.items():
    if not landscape:
        continue
    gammas = landscape['gammas']
    betas = landscape['betas']
    exp_costs = np.array(landscape['landscape'])
    betas_, gammas_ = np.meshgrid(betas, gammas)

    fig = plt.figure()
    ax  = fig.gca(projection='3d')
    ax.set_xlabel(r'$\gamma$')
    ax.set_ylabel(r'$\beta$')
    ax.set_zlabel('Expected costs')
    surf = ax.plot_surface(gammas_, betas_, exp_costs, cmap=cm.coolwarm, rstride=1, cstride=1, alpha=None, antialiased=True)
    plt.title(str(problem))
    if show_plots: plt.show()
    problem_string = problem_dict2str(eval(problem))
    plt.savefig(f'plots/landscape/{noise_string}/landscape-{noise_string}-{problem_string}')

#%% 
# analytic_constants_problems = []
# for problem in unique_problems:
#     _, _, _, A, B, C = integer_bin_packing(**problem)
#     analytic_constants_problems.append({**problem, 'A': A, 'B': B, 'C': C})

# analytic_constants_data = {}
# conditions_ = {'noise': True, 'success': False}
# for problem in analytic_constants_problems:
#     conditions = {'problem': problem, **conditions_}
#     analytic_constants_data[str(problem)] = filter_data(data.values(), conditions)
