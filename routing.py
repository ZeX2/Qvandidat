from funcs import *
from integer_bin_packing import *

# For save_results
import sys
import os
import json
import scipy.io
import numpy as np
from datetime import timedelta, datetime
#from problem_list import get_problem_list
from problem_list_routing import get_problem_list


# TODO
# Make sure run_chalmers_circuit_ideal and expected_value returns 
# identical results
MAX_ITER = 10

def main(problem_number):
    print(problem_number)

    # prioritized order
    problem_list = get_problem_list()
    problem_dict = problem_list[problem_number]
    _run_problem(**problem_dict)


def _run_problem(W,W_max,p,routing):
    J, h, const, A, B, C = integer_bin_packing(W, W_max)
    S = {'W':W, 'W_max':W_max,'A':A, 'B':B, 'C':C}
    file_suffix = '-routing-' + routing + '-' + str(S) + '-' + str(int(datetime.now().timestamp()))

    n = len(W) * len(W) + len(W) * W_max

    if routing == 'star' and n > 5:
        print('Star routing method is only defined for n <= 5')
        return

    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, np.trace(J))/B for bits in bits_list}
    
    for iter_ in range(1,MAX_ITER+1):
        # TODO Set shots to reasonable value
        print('Finding optimal angles for p =', str(p), 'using', routing, 'for', str(S))
        start_time = time.monotonic()
        gammas, betas, opt_result = optimize_angles_routing(J, h, p, routing, costs, maxiter=50, shots=10000)
        end_time = time.monotonic()
        opt_dict = {'nfev':opt_result.nfev,'message':opt_result.message,'success':opt_result.success,'nit':opt_result.nit,'routing':routing}
        file_name = 'angles-p' + str(p) + '-iter-' + str(iter_) + file_suffix
        save_results(gammas, betas, opt_result.fun, str(S), end_time-start_time, file_name,opt_dict)


def save_results(gammas, betas, fun, problem, dt=-1, file_name=None, extra_data={}, save_mat=True, save_json=True):
    p = len(gammas)
    
    dt_str = str(timedelta(seconds=dt))
    data = {'expected_value':fun, 'optimal_gammas':gammas, \
            'optimal_betas':betas, 'problem_identifier':problem, \
            'now':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
            'execution_time':dt_str}

    data.update(extra_data)

    if file_name is None: 
        file_name = 'unkown-' + problem + '-' + str(str(int(datetime.now().timestamp())))

    print('Found optimal angles for', problem, 'after running for', dt_str, 'saved to file', file_name)
    file_name = file_name.replace(':','_')
    file_name = os.path.join('data', file_name)
    os.makedirs('data', exist_ok=True)

    if save_mat:
        scipy.io.savemat(file_name + '.mat', data)

    if save_json:
        with open(file_name + '.json', 'w') as fp:
            json.dump(data, fp, indent=4, cls=NumpyEncoder)
    
    return data


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':

    main(int(sys.argv[1]))


