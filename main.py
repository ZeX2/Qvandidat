from funcs import *
from integer_bin_packing import *

# For save_results
import sys
import os
import json
import scipy.io
import numpy as np
from datetime import timedelta, datetime


# TODO
# Make sure run_chalmers_circuit_ideal and expected_value returns 
# identical results
MAX_ITER = 10

def main(problem_number):
    print(problem_number)
    problem_list = [{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 1, 'noise': False},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 2, 'noise': False},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 3, 'noise': False}, # test
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 4, 'noise': False},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 5, 'noise': False},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 6, 'noise': False},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 7, 'noise': False},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 1, 'noise': True},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 2, 'noise': True},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 3, 'noise': True},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 4, 'noise': True},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 5, 'noise': True},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 6, 'noise': True},
{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 12, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 576, 'p': 1, 'noise': False},
{'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 576, 'p': 2, 'noise': False},
{'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 576, 'p': 3, 'noise': False},
{'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 576, 'p': 4, 'noise': False},
{'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 576, 'p': 5, 'noise': False},
{'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 576, 'p': 6, 'noise': False},
{'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 576, 'p': 7, 'noise': False},
{'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 324, 'p': 1, 'noise': True},
{'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 324, 'p': 2, 'noise': True},
{'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 324, 'p': 3, 'noise': True},
{'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 324, 'p': 4, 'noise': True},
{'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 324, 'p': 5, 'noise': True},
{'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 324, 'p': 6, 'noise': True},
{'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 324, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 16, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 16, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 16, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 16, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 16, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 16, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 16, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 80, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 80, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 80, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 80, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 80, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 80, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 80, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 144, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 144, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 144, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 144, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 144, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 144, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 144, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 208, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 208, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 208, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 208, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 208, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 208, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 48, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 8, 'B': 4, 'C': 208, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 48, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 48, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 48, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 48, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 48, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 48, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 240, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 240, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 240, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 240, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 240, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 240, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 240, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 432, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 432, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 432, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 432, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 432, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 432, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 432, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 624, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 624, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 624, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 624, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 624, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 624, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 24, 'B': 4, 'C': 624, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 80, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 80, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 80, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 80, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 80, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 80, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 80, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 400, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 400, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 400, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 400, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 400, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 400, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 400, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 720, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 720, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 720, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 720, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 720, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 720, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 720, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 1040, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 1040, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 1040, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 1040, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 1040, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 1040, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 40, 'B': 4, 'C': 1040, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 112, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 112, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 112, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 112, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 112, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 112, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 112, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 560, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 560, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 560, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 560, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 560, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 560, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 560, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1008, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1008, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1008, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1008, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1008, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1008, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1008, 'p': 7, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1456, 'p': 1, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1456, 'p': 2, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1456, 'p': 3, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1456, 'p': 4, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1456, 'p': 5, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1456, 'p': 6, 'noise': True},
{'W_max': 2, 'W': [1, 1], 'A': 56, 'B': 4, 'C': 1456, 'p': 7, 'noise': True}
]
    # prioritized order
    problem_dict = problem_list[problem_number]
    if problem_dict['noise']:
        del problem_dict['noise']
        #_run_problem_simul(**problem_dict)
        _run_problem_state(**problem_dict)
        
    else:
        del problem_dict['noise']
        #_run_problem_state(**problem_dict)
        
    


def _run_problem_simul(W,W_max,p,A = None,B = None, C = None):
    S = {'W':W, 'W_max':W_max,'A':A, 'B':B, 'C':C}
    file_suffix = '-simul-' + str(S) + '-' + str(int(datetime.now().timestamp()))

    J, h, const, A, B, C = integer_bin_packing(W, W_max, A, B, C)
    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, np.trace(J))/B for bits in bits_list}
    if p==1:
        print('Running noisy simulations for', str(S))
    
        print('Creating lanscape')
        start_time = time.monotonic()
        # TODO Set shots to reasonable value
        # TODO Set iter_ to a good value
        gammas, betas, exp_costs = landscape_simul(J, h,costs, iter_=5000, shots=5000)
        end_time = time.monotonic()
    
        file_name = 'landscape' + file_suffix
        save_results(gammas, betas, -1, str(S), end_time-start_time, file_name, {'landscape':exp_costs})

    
    for iter_ in range(1,MAX_ITER+1):
        # TODO Set shots to reasonable value
        print('Finding optimal angles for p =', str(p))
        start_time = time.monotonic()
        gammas, betas, opt_result = optimize_angles_simul(J, h, p, costs, maxiter=int(p**(3/2))*1000, shots=10000)
        end_time = time.monotonic()
        opt_dict = {'nfev':opt_result.nfev,'message':opt_result.message,'success':opt_result.success,'nit':opt_result.nit}
        file_name = 'angles-p' + str(p) + '-iter-' + str(iter_) + file_suffix
        save_results(gammas, betas, opt_result.fun, str(S), end_time-start_time, file_name,opt_dict)


     
def _run_problem_state(W,W_max,p , A = None,B = None, C = None):
    S = {'W':W, 'W_max':W_max,'A':A, 'B':B, 'C':C}
    file_suffix = '-state-' + str(S) + '-' + str(int(datetime.now().timestamp()))

    J, h, const, A, B, C = integer_bin_packing(W, W_max, A, B, C)
    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, np.trace(J))/B for bits in bits_list}
    if p ==1:
        print('Running statevector simulations for', str(S))
    
        print('Creating lanscape')
    
        start_time = time.monotonic()
        # TODO Set iter_ to a good value
        gammas, betas, exp_costs = landscape_state(J, h,costs, iter_=5000)
        end_time = time.monotonic()
    
        file_name = 'landscape' + file_suffix
        save_results(gammas, betas, -1, str(S), end_time-start_time, file_name, {'landscape':exp_costs})

    #for p in range(1,MAX_P+1):
    for iter_ in range(1,MAX_ITER+1):
        print('Finding optimal angles for p =', str(p))
        start_time = time.monotonic()
        gammas, betas, opt_result = optimize_angles_state(J, h, p, costs, maxiter=int(p**(3/2))*1000)
        end_time = time.monotonic()

        file_name = 'angles-p' + str(p) + '-iter-' + str(iter_) + file_suffix
        opt_dict = {'nfev':opt_result.nfev,'message':opt_result.message,'success':opt_result.success,'nit':opt_result.nit}
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


