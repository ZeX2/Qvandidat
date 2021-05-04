from funcs import *
from integer_bin_packing import *

# For save_results
import sys
import os
import json
import scipy.io
import numpy as np
from datetime import timedelta, datetime
import ast # maybe this is a bad idea, idk

# TODO
# Make sure run_chalmers_circuit_ideal and expected_value returns 
# identical results


def main():
        
    # for each file in folder, read JSON
    for filename in os.listdir('data'):
        if not filename.endswith('.json'): continue


        filepath = os.path.join('data', filename) 

        print(filename)
        with open(filepath) as json_file:
            data = json.load(json_file)

        if 'landscape' in filename:
            print(filename)
            print(data)
            landscape = data['landscape']
            gammas = data['optimal_gammas']
            betas = data['optimal_betas']
            
            indices = np.argwhere(landscape == np.min(landscape))
            print(indices)
            print(gammas[indices[0][0]])
            print(betas[indices[0][1]])

            optimal_gammas = gammas[indices[0][0]]
            optimal_betas = betas[indices[0][1]]

            data['optimal_gammas'] = optimal_gammas
            data['optimal_betas'] = optimal_betas

            data['gammas'] = gammas
            data['betas'] = betas

        continue
        problem_identifier = data['problem_identifier']
        S = ast.literal_eval(problem_identifier)
        print(S)

        J, h, const, A, B, C = integer_bin_packing(**S)
        bits_list = get_bits_list(len(J))
        costs = {bits: cost_function(bits, J, h, const, np.trace(J))/B for bits in bits_list}

        optimal_gammas = data['optimal_gammas']
        optimal_betas = data['optimal_betas']
        
        if 'state' in filename:
            prob_dist = probability_cost_distribution_state(optimal_gammas, optimal_betas, J, h, costs)
            appr_ratio = approximation_ratio_state(optimal_gammas, optimal_betas, J, h, costs)

        if 'simul' in filename:
            prob_dist = probability_cost_distribution_simul(optimal_gammas, optimal_betas, J, h, costs, shots=10000)
            appr_ratio = approximation_ratio_simul(optimal_gammas, optimal_betas, J, h, costs, shots=10000)

        else:
            print('Invalid file, file name needs to contain either state or simul')
            continue
        
        data['probability_distribution'] = prob_dist
        data['approximation_ratio'] = appr_ratio
        
        save_results(filename, data)


def save_results(file_name, results, save_mat=True, save_json=True):
    print('Saving results for', results['problem_identifier'])

    file_name = os.path.join('results', file_name)
    os.makedirs('results', exist_ok=True)

    if save_mat:
        scipy.io.savemat(file_name + '.mat', results)

    if save_json:
        with open(file_name + '.json', 'w') as fp:
            json.dump(results, fp, indent=4, cls=NumpyEncoder)
    
    return results


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':

    main()


