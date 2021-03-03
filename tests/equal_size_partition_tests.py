import numpy as np
from equal_size_partition.decode_state import decode_state
from equal_size_partition.get_ising_model import get_ising_model
from equal_size_partition.get_circuit import get_circuit
from equal_size_partition.get_cost_function import get_cost_function
from equal_size_partition.get_chalmers_circuit import get_chalmers_circuit
from equal_size_partition.get_expectation_value import expectation_value
from classical_optimizers.global_search_algorithms import shgo
from classical_optimizers.global_search_algorithms import bruteforce
from classical_optimizers.global_search_algorithms import differential_evolution

def get_objecvtive(S):

    (J, h, bound) = get_ising_model(S)
    cost_function = get_cost_function(J, h, S)


    def objective(x):
        # if instnace of ndarray
        p = int(len(x)/2)
        print(x)

        gammas = x[0:p]
        betas = x[p:2*p]

        qc = get_circuit(gammas, betas, J, h)
        cqc = get_chalmers_circuit(qc)

        (exp_val, z_best) = expectation_value(cqc,
                cost_function, repetitions=10000)

        return exp_val

def run_all_tests():

    dataset = [np.array([1,2, 4, 3])] 
    
    for i,S in enumerate(dataset):
        objective = get_objecvtive(S)

        bruteforce(objective, [bound, bound], max_evaluations=10000,
                plot=True,save_file='bruteforce'+str(i))


        differential_evolution_p(objective, bound, p=1)
        differential_evolution_p(objective, bound, p=2)
        differential_evolution_p(objective, bound, p=3)
        differential_evolution_p(objective, bound, p=4)

        shgo_p(objective, bound, p=1)
        shgo_p(objective, bound, p=2)
        shgo_p(objective, bound, p=3)
        shgo_p(objective, bound, p=4)
        
    

    return

def shgo_p(objective, bound, p):
    return shgo(objective, [bound] * p)

def differential_evolution_p(objective, bound, p):
    return differential_evolution(objective, [bound] * p)


