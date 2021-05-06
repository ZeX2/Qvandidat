from integer_bin_packing import *


MAX_P = 7

def main():
    # prioritized order
    print('[')
    run_problem([1], 1, A = 8) #8 qubits
    run_problem([1, 1], 2, A = 32) #8 qubits
    run_problem([1, 1, 1], 1, A = 12)  #12 qubits
    #run_problem([1, 2, 3], 3, noise = False, test_const=False) #18 qubits
    #run_problem([1 ,2], 2, noise = False, test_const=False) #8 qubits
    #run_problem([1 ,6], 6, noise = False, test_const=False) #16 qubits
    print(']')
    
    
def run_problem(W, W_max, A):
    _run_problem_simul(W,W_max, A = A, B = 4, C = A)
    _run_problem_simul(W,W_max, A = A, B = 4, C = 2*A)
    _run_problem_simul(W,W_max, A = A, B = 4, C = 4*A)

    _run_problem_state(W,W_max, A = A, B = 4, C = A)
    _run_problem_state(W,W_max, A = A, B = 4, C = 2*A)
    _run_problem_state(W,W_max, A = A, B = 4, C = 4*A)

def _run_problem_simul(W,W_max, A = None,B = None, C = None):
    J, h, const, A, B, C = integer_bin_packing(W, W_max, A, B, C)

    for p in range(1,MAX_P+1):
        problem_dict = {'W_max': W_max, 'W': W, 'A': A, 'B': B, 'C': C, 'p':p, 'noise':True}
        print(str(problem_dict) + ',')

     
def _run_problem_state(W,W_max, A = None,B = None, C = None):
    J, h, const, A, B, C = integer_bin_packing(W, W_max, A, B, C)

    for p in range(1,MAX_P+1):
        problem_dict = {'W_max': W_max, 'W': W, 'A': A, 'B': B, 'C': C, 'p':p, 'noise':False}
        print(str(problem_dict) + ',')


if __name__ == '__main__':
    main()


