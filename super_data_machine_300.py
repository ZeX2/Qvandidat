import os
import json
from statistics import mean

import numpy as np
import matplotlib.pyplot as plt

from integer_bin_packing import *
from funcs import *

def filter_data(data, conditions):
    return list(filter(lambda item: all(((k in item and item[k]==v)for (k,v) in conditions.items())), data))

def time_in_sec(time):
    h, m, s = [float(i) for i in time.split(':')]
    return int(3600*h + 60*m + s)

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
#Best expected costs and approximation ratio vs p for all noise instances

instances_data = {}
conditions_ = {'noise': False, 'success': True}
for instance in unique_instances:
    conditions = {'problem': instance, **conditions_}
    instances_data[str(instance)] = filter_data(data.values(), conditions)

exp_data = {}
approx_ratio_data = {}
optimal_prob_data = {}
valid_prob_data = {}
avg_time_data = {}
#Staplar?

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
    exp_costs = []
    approx_ratio = []
    optimal_probs = []
    valid_probs = []
    avg_times = []

    for p in p_values:
        exp_costs.append(min(instance['expected_value'] for instance in instances if instance['p']==p))
        approx_ratio.append(max(instance['approximation_ratio'] for instance in instances if instance['p']==p))
        optimal_probs.append(max(instance['probability_distribution'][str(min_cost)] 
                                 if (instance['p']==p and str(min_cost) in instance['probability_distribution']) else 0
                                 for instance in instances))
        valid_probs.append(max(sum(float(prob) for cost, prob in instance['probability_distribution'].items() 
                                   if float(cost) <= max_valid_cost)
                               for instance in instances if instance['p']==p))
        avg_times.append(mean(time_in_sec(instance['execution_time']) for instance in instances if instance['p']==p))

    exp_data[problem] = (p_values, exp_costs)
    approx_ratio_data[problem] = (p_values, approx_ratio)
    optimal_prob_data[problem] = (p_values, optimal_probs)
    valid_prob_data[problem] = (p_values, valid_probs)
    avg_time_data[problem] = (p_values, avg_times)

#%% Plotting

# Expected value vs p
for problem, plot_data in exp_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1], '-o')
    plt.ylabel('Best expected cost')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.show()

# Approximation ratio vs p
for problem, plot_data in approx_ratio_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1], '-o')
    plt.ylabel('Best approximation ratio')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.show()

# Probability of optimal solution vs p
for problem, plot_data in optimal_prob_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1], '-o')
    plt.ylabel('Probability of optimal solution')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.show()
    plt.plot()
    
# Probability of valid solution vs p
for problem, plot_data in valid_prob_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1], '-o')
    plt.ylabel('Probability of valid solution')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.show()
    plt.plot()

# Average execution time vs p
for problem, plot_data in avg_time_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1], '-o')
    plt.ylabel('Average execution time (s)')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.show()
    plt.plot()

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
