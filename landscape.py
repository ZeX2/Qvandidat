from funcs import *
from integer_bin_packing import *
from main import *

# For save_results
#from problem_list import get_problem_list
from problem_list_landscape import get_problem_list


def main(problem_number):
    print(problem_number)

    # prioritized order
    problem_list = get_problem_list()
    problem_dict = problem_list[problem_number]

    if problem_dict['noise']:
        del problem_dict['noise']
        _run_landscape_simul(**problem_dict)
    else:
        del problem_dict['noise']
        _run_landscape_state(**problem_dict)


def _run_landscape_simul(W,W_max,p,A = None,B = None, C = None):
    S = {'W':W, 'W_max':W_max,'A':A, 'B':B, 'C':C}
    file_suffix = '-simul-' + str(S) + '-' + str(int(datetime.now().timestamp()))

    J, h, const, A, B, C = integer_bin_packing(W, W_max, A, B, C)
    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, np.trace(J))/B for bits in bits_list}
   
    print('Creating landscape with simulation for', str(S))
    start_time = time.monotonic()
    gammas, betas, exp_costs = landscape_simul(J, h,costs, step_size=0.01, shots=5000)
    end_time = time.monotonic()

    file_name = 'landscape' + file_suffix
    save_results(gammas, betas, -1, str(S), end_time-start_time, file_name, {'landscape':exp_costs})

     
def _run_landscape_state(W,W_max,p , A = None,B = None, C = None):
    S = {'W':W, 'W_max':W_max,'A':A, 'B':B, 'C':C}
    file_suffix = '-state-' + str(S) + '-' + str(int(datetime.now().timestamp()))

    J, h, const, A, B, C = integer_bin_packing(W, W_max, A, B, C)
    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, np.trace(J))/B for bits in bits_list}

    print('Creating landscape with statevector for', str(S))
    start_time = time.monotonic()
    gammas, betas, exp_costs = landscape_state(J, h,costs, step_size=0.01)
    end_time = time.monotonic()

    file_name = 'landscape' + file_suffix
    save_results(gammas, betas, -1, str(S), end_time-start_time, file_name, {'landscape':exp_costs})


if __name__ == '__main__':

    #main(int(sys.argv[1]))
    for i in range(0, 19):
        main(i)


