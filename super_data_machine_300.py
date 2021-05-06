import os
import json

import numpy as np
import matplotlib.pyplot as plt

from integer_bin_packing import *


def filter_data(data, conditions):
    return list(filter(lambda item: all(((k in item and item[k]==v)for (k,v) in conditions.items())), data))

dir_path = os.getcwd()
data_path = os.path.join(dir_path, 'results')
data_json = [f for f in os.listdir(data_path) if f.endswith('.json.json')]

data = {}
for file_name in data_json:
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


#%% Best expected costs vs p for all noise instances
noise_instances_data = {}
conditions_ = {'noise': True, 'success': True}
for instance in unique_instances:
    conditions = {'problem': instance, **conditions_}
    noise_instances_data[str(instance)] = filter_data(data.values(), conditions)


noise_plot_data = {}
for problem, instances in noise_instances_data.items():
    if not instances:
        continue
    p_values = sorted(list({instance['p'] for instance in instances}))
    exp_costs = []
    for p in p_values:
        exp_costs.append(max(instance['expected_value'] for instance in instances if instance['p']==p))
    noise_plot_data[problem] = (p_values, exp_costs)


for problem, plot_data in noise_plot_data.items():
    plt.figure()
    plt.plot(plot_data[0], plot_data[1], '-o')
    plt.ylabel('Best expected cost')
    plt.xlabel('p')
    plt.title(str(problem))
    plt.show()


#%%
analytic_constants_problems = []
for problem in unique_problems:
    _, _, _, A, B, C = integer_bin_packing(**problem)
    analytic_constants_problems.append({**problem, 'A': A, 'B': B, 'C': C})

analytic_constants_data = {}
conditions_ = {'noise': True, 'success': False}
for problem in analytic_constants_problems:
    conditions = {'problem': problem, **conditions_}
    analytic_constants_data[str(problem)] = filter_data(data.values(), conditions)
