from funcs import *
from integer_bin_packing import *
def main():
    #TODO run_problem for different problems.
    
def run_problem(W,W_max, noise = False, test_const = False):
    if noise:
        exit(0)
    if test_const:
        B = 4
        for a in range(2,12,2):
            for c in range(2,26,4):
                 _run_problem(W,W_max,A = a*B, B=B, C=c*a*B)
    _run_problem(W,W_max)        
     
def _run_problem(W,W_max, A = None,B = None, C = None):
    J, h, const, A, B, C = integer_bin_packing(W, W_max, A, B, C)
    for p in range(1,11):
        for iter_ in range(1,11):
            angles = optimize_angles_state(J, h, p, costs, maxiter=p**2*1000)
            #TODO save data, now it overwrites
            #TODO time and performance data

if __name__ == '__main__':
    main()