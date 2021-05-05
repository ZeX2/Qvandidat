# -*- coding: utf-8 -*-
"""
Created on Wed May  5 19:11:53 2021

@author: Isak Brundin
"""
import os
import json
import ast

from integer_bin_packing import *
from funcs import *

from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram

BACKEND = Aer.get_backend('unitary_simulator')
SIMULATOR = Aer.get_backend('qasm_simulator')
SVSIM = Aer.get_backend('statevector_simulator')


def get_data_for_p(p,problem_instance,true_constant=False,path=False):
    search_string = "angles-p"+str(p)
    print(search_string)
    file_list = list()
    if not path:
        path = "C:\\Users\\Isak Brundin\\Downloads\\Qvandidat-data-analysis\\Qvandidat-data-analysis\\data"
    all_files = os.listdir(path)
    
    for file_name in all_files:
        if search_string in file_name and file_name.endswith('.json'):
            
            if "'W'_ [1]" in file_name and problem_instance == 1:
                file_list.append(os.path.join(path,file_name))
                print("h1j")
            elif "'W'_ [1, 1]" in file_name and problem_instance == 2:
                print("h2j")
                file_list.append(os.path.join(path,file_name))
            elif "'W'_ [1, 1, 1]" in file_name and problem_instance == 3:
                file_list.append(os.path.join(path,file_name))
            else:
                print("nej")
    if true_constant:
        true_constant_file_list = list()
        for file_ in file_list:    
            if true_constant == int(file_.split("'A'_ ")[1].split(", 'B'_ ")[0]):

                true_constant_file_list.append(file_)
   
        return true_constant_file_list
    return file_list
def data_extracter(json_file):
    with open(json_file) as f:
    
        data_dict = json.load(f)

    problem_dict = ast.literal_eval(data_dict["problem_identifier"])
    J,h,const,A,B,C = integer_bin_packing(problem_dict["W"],problem_dict["W_max"],problem_dict["A"],problem_dict["B"],problem_dict["C"])
    TrJ = np.trace(J)
    bits_list = get_bits_list(len(J))
    costs = {bits: cost_function(bits, J, h, const, TrJ)/B for bits in bits_list}
    qc = qaoa_ising_circuit(J, h, data_dict["optimal_gammas"],data_dict["optimal_betas"], measure=False)
    sv = execute(qc, SVSIM).result().get_statevector()
    sv = Statevector(sv)
    prob_dict = sv.probabilities_dict()
    costs_freq = dict()
    for bits, prob in prob_dict.items():
        cost = costs[bits]
        if cost not in costs_freq:
            costs_freq[cost] = prob
        else:
            costs_freq[cost] += prob
    print(costs_freq)
    return costs_freq
def extracted_data_for_p(json_list):
    p1W11json =list()
    for i in range(len(json_list)):
        p1W11json.append(data_extracter(json_list[i]))
        i+=1
    return p1W11json

def best_optimal(costs_list,histogram = False,optimal_cost = 1.0):
    true_prob = 0
    true_prob_dict = {}
    
    for i in range(len(costs_list)):
        try:
            curr_prob = costs_list[i][optimal_cost]
        except:
            curr_prob = 0
        if curr_prob>true_prob:
            print(true_prob)
            true_prob = curr_prob
            true_prob_dict = costs_list[i]
    if histogram:
        plot_histogram(true_prob_dict)
    return true_prob_dict,true_prob

def avg_costs(costs_list,optimal_cost = 1.0):
    avg_dict = {}
    for i in range(len(costs_list)):
        for cost,prob in costs_list[i].items():
            if cost not in avg_dict:
                avg_dict[cost] = prob
            else:
                avg_dict[cost] += prob
    for cost,prob in avg_dict.items():
        avg_dict[cost] = avg_dict[cost]/float(len(costs_list))
    try:
        optimal_prob = avg_dict[optimal_cost]
    except:
        optimal_prob =0
    return avg_dict,optimal_prob

#&&
# Example on how to run
path = "C:\\Users\\Isak Brundin\\Downloads\\Qvandidat-data-analysis\\Qvandidat-data-analysis\\data"
#gets all files with given problem and p
# problem_instance = 1 is the problem W=[1],W_max =1
# problem_instance = 2 is the problem W=[1,1],W_max =2
# problem_instance = 3 is the problem W=[1,1,1],W_max =1
# true constant is False by default, then all files with the problem instance will merge
# if a specific A is wanted set true constant to it

p1W11 = get_data_for_p(1,2,path = path,true_constant = 8)
p1W11json = extracted_data_for_p(p1W11)
# gives the angles that yielded the highest probability for optimal solution
best_test_dictp1,best_test_probp1=best_optimal(p1W11json,histogram = True)
# averages over all files
avg_test_dictp1,avg_test_optimalp1 = avg_costs(p1W11json)

p2W11 = get_data_for_p(2,2,path = path,true_constant = 8)
p3W11 = get_data_for_p(3,2,path = path,true_constant = 8)
p4W11 = get_data_for_p(4,2,path = path,true_constant = 8)
p5W11 = get_data_for_p(5,2,path = path,true_constant = 8)
p6W11 = get_data_for_p(6,2,path = path,true_constant = 8)

p