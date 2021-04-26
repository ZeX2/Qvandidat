from funcs import *
from integer_bin_packing import *

# For save_results
import os
import json
import scipy.io
import numpy as np
from datetime import timedelta, datetime


# TODO
# Make sure run_chalmers_circuit_ideal and expected_value returns 
# identical results


def main():
    # TODO Investigate why generate circuit isn't working.
    run_problem([1, 1], 2, noise=False, test_const=False)
    #run_problem([1, 1], 2, noise=True, test_const=True)
    #TODO run_problem for different problems.

    run_problem([1], 1, noise=False, test_const=False)

    run_problem([1, 1, 1], 1, noise=True, test_const=True)
    
def run_problem(W,W_max, noise = False, test_const = False):
    if noise:
        exit(0)
    if test_const:
        B = 4
        for a in range(2,12,2):
            for c in range(2,26,4):
                 _run_problem_state(W,W_max,A = a*B, B=B, C=c*a*B)

    _run_problem_simul(W,W_max)
    _run_problem_state(W,W_max)
    

def _run_problem_simul(W,W_max, A = None,B = None, C = None):
    S = {'W':W, 'W_max':W_max,'A':A, 'B':B, 'C':C}
    file_suffix = '-simul-' + str(S) + '-' + str(int(datetime.now().timestamp()))

    J, h, const, A, B, C = integer_bin_packing(W, W_max, A, B, C)
    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, np.trace(J))/B for bits in bits_list}

    start_time = time.monotonic()
    # TODO Set shots to reasonable value
    # TODO Set iter_ to a good value
    gammas, betas, exp_costs = landscape_simul(J, h,costs, iter_=5000, shots=5000)
    end_time = time.monotonic()

    file_name = 'landscape' + file_suffix
    save_results(gammas, betas, -1, str(S), end_time-start_time, file_name, {'landscape':exp_costs})

    for p in range(1,11):
        for iter_ in range(1,11):
            # TODO Set shots to reasonable value
            start_time = time.monotonic()
            gammas, betas, exp_val = optimize_angles_simul(J, h, p, costs, maxiter=p**2*1000, shots=10000)
            end_time = time.monotonic()

            file_name = 'angles-p' + str(p) + '-iter-' + str(iter_) + file_suffix
            save_results(gammas, betas, exp_val, str(S), end_time-start_time, file_name)


     
def _run_problem_state(W,W_max, A = None,B = None, C = None):
    S = {'W':W, 'W_max':W_max,'A':A, 'B':B, 'C':C}
    file_suffix = '-state-' + str(S) + '-' + str(int(datetime.now().timestamp()))

    J, h, const, A, B, C = integer_bin_packing(W, W_max, A, B, C)
    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, np.trace(J))/B for bits in bits_list}

    start_time = time.monotonic()
    # TODO Set iter_ to a good value
    gammas, betas, exp_costs = landscape_state(J, h,costs, 5000)
    end_time = time.monotonic()

    file_name = 'landscape' + file_suffix
    save_results(gammas, betas, -1, str(S), end_time-start_time, file_name, {'landscape':exp_costs})

    for p in range(1,11):
        for iter_ in range(1,11):
            start_time = time.monotonic()
            gammas, betas, exp_val = optimize_angles_state(J, h, p, costs, maxiter=p**2*1000)
            end_time = time.monotonic()

            file_name = 'angles-p' + str(p) + '-iter-' + str(iter_) + file_suffix
            save_results(gammas, betas, exp_val, str(S), end_time-start_time, file_name)


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
    main()


