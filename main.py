import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
#%matplotlib agg

from tqdm import tqdm

from integer_bin_packing import *
from equal_size_partition import *
from funcs import *

#%% Bin packing
# Item weights
W = [1, 1]
# Max weight of bin
W_max = 2
J, h, const, A, B, C = integer_bin_packing(W, W_max, C_factor=3)
TrJ = np.trace(J)

bits_list = get_bits_list(len(J))
costs = {bits: cost_function(bits, J, h, const, TrJ)/B for bits in bits_list}

#%% Equal Size Partition
# S = [1, 2, 3, 4]
# J, h, const = equal_size_partition(S)
# TrJ = np.trace(J)

#%% Optimization
p = 5 # Sets the p-level
out = True #Set this to True to have continous update on the optimization
angles, cost = optimize_angles(p, J, h, const, TrJ, costs, out=out)
print(angles)
print(cost)

#%%
# [1, 1], 2, C = 2A, 
expected_cost(J, h, const, TrJ, 3.12225594, 0.30371598, costs, histogram=True,probs=True)
expected_cost(J, h, const, TrJ, [3.15812491, 1.25654823], [2.71176354, 0.27240049], costs, histogram=True,probs=True)
expected_cost(J, h, const, TrJ, [1.03095384, 1.0867246 , 2.59478705], [1.5460229 , 3.1757417 , 2.35685995], costs, histogram=True)
expected_cost(J, h, const, TrJ, [0.99576246, 2.13449288, 5.32455158, 1.18130696], [4.62583989, 2.00279267, 4.36280221, 0.4709013], costs, histogram=True)
expected_cost(J, h, const, TrJ, [2.36944458, 1.17249538, 0.410751, 0.66790066, 1.91204215], [1.61679967, 3.96129773, 1.30548718, 0.24146866, 1.63173029], costs, histogram=True)
expected_cost(J, h, const, TrJ, [5.2888701, 0.2140996, 0.35869375, 1.77861308, 2.59985261, 2.30950479], [1.62633299, 2.62556142, 1.2353983, 0.4110642, 1.77331014, 3.14159265], costs, histogram=True)
expected_cost(J, h, const, TrJ, [4.681126, 1.96548122, 1.40945676, 0., 5.65443637, 2.35333539, 2.94090352], [2.85699416, 1.91240846, 1.37397275, 1.3255589, 2.77777898, 0.96111532, 2.61819194], costs, histogram=True)
expected_cost(J, h, const, TrJ, [4.50533816, 0.61417329, 4.34056327, 0.52574006, 2.6101065, 1.55520545, 4.96265275, 0.78157716], [0.20469296, 2.24862138, 3.26560563, 1.49979025, 5.59152463,2.44741017, 5.90621296, 0.16447593], costs, histogram=True)

# [1, 1], 2, C=A
expected_cost(J, h, const, TrJ, [2.72039455, 1.39302597, 3.93021204, 2.07757555, 0.02526551], [1.56189776, 1.90686837, 2.12362766, 4.71443538, 1.40428264], costs, histogram=True)

# [1 1], 2, C=3A
expected_cost(J, h, const, TrJ, 3.16314244, 2.83650637, costs, histogram=True)

#%% Profile optimization
def main():
    p = 1 # Sets the p-level
    out = True #Set this to True to have continous update on the optimization
    angles, cost = optimize_angles(p, J, h, const, TrJ, costs, out=out)

#%% Run simulation for several (gamma, beta) where p = 1
plt.switch_backend("Qt5Agg")
s = 0.1; 
gammas = np.arange(0, 2*np.pi, s)
betas = np.arange(0, np.pi, s)
avg_costs = np.zeros((len(gammas), len(betas)))

print('Running simulations...')
for i in tqdm(range(len(gammas))):
    for j in range(len(betas)):
        avg_costs[i,j] = run_simulation(J, h, const, TrJ, gammas[i], betas[j], shots=1000)/B

betas_, gammas_ = np.meshgrid(betas, gammas)

fig = plt.figure()
ax  = fig.gca(projection='3d')
ax.set_xlabel(r'$\gamma$')
ax.set_ylabel(r'$\beta$')
ax.set_zlabel('Negative costs')
surf = ax.plot_surface(gammas_, betas_, -avg_costs, cmap=cm.coolwarm, linewidth=0, antialiased=True)
#ax.scatter(3.4, 3.5, -0.261, color="k", s=50)
plt.show()

min_cost = np.amin(avg_costs)
i, j = np.where(avg_costs == min_cost)
i, j = i[0], j[0]
print(f'Best angles: ({gammas[i]}, {betas[j]})')
print('Minimum average cost for best angels:', min_cost)

#%% Run simulation for several (gamma, beta) where p = 2
s = 0.1; 
gammas_1 = np.arange(0, np.pi, s)
betas_1 = np.arange(0, np.pi, s)
gammas_2 = np.arange(0, np.pi, s)
betas_2 = np.arange(0, np.pi, s)
avg_costs = np.zeros((len(gammas_1), len(betas_1), len(gammas_2), len(betas_2)))

print('Running simulations...')
for i in range(len(gammas_1)):
    for j in range(len(betas_1)):
        for k in range(len(gammas_2)):
            for l in range(len(betas_2)):
                gamma = [gammas_1[i], gammas_2[k]]
                beta = [betas_1[j], betas_2[l]]
                avg_costs[i,j,k,l] = run_simulation(J, h, const, TrJ, gamma, beta, shots=500)/B

min_cost = np.amin(avg_costs)
i, j, k, l = np.where(avg_costs == min_cost)
i, j, k, l = i[0], j[0], k[0], l[0]
print(f'Best angles: ([{gammas_1[i]}, {gammas_2[ik]}], [{betas_1[j]}, {betas_2[l]}])')
print('Minimum average cost for best angels:', min_cost)

#%% Expected costs  for p = 1
s = 0.1; 
gammas = np.arange(0, 2*np.pi, s)
betas = np.arange(0, np.pi, s)
exp_costs = np.zeros((len(gammas), len(betas)))

print('Running simulations...')
for i in tqdm(range(len(gammas)), desc='Loop i', position=0):
    for j in range(len(betas)):
        exp_costs[i,j] = expected_cost(J, h, const, TrJ, gammas[i], betas[j], costs)

betas_, gammas_ = np.meshgrid(betas, gammas)

fig = plt.figure()
ax  = fig.gca(projection='3d')
ax.set_xlabel(r'$\gamma$')
ax.set_ylabel(r'$\beta$')
ax.set_zlabel('Negative costs')
surf = ax.plot_surface(gammas_, betas_, -exp_costs, cmap=cm.coolwarm, linewidth=0, antialiased=True)
#ax.scatter(3.4, 3.5, -0.261, color="k", s=50)
plt.show()

min_cost = np.amin(exp_costs)
i, j = np.where(exp_costs == min_cost)
i, j = i[0], j[0]
print(f'Best angles: ({gammas[i]}, {betas[j]})')
print('Minimum average cost for best angels:', min_cost)

#%%
#Optimal value for [1 1] and 1
expected_cost(J, h, const, TrJ, 4, 0.8, costs, histogram=True)
run_simulation(J, h, const, TrJ, 4, 0.8, shots=1000000, histogram=True)/B

#Optimal value for [1 1] and 2
expected_cost(J, h, const, TrJ, 5.9, 0.4, costs, histogram=True)
run_simulation(J, h, const, TrJ, 5.9, 0.4, shots=1000000, histogram=True)/B

#%% Expected costs  for p = 2
s = 0.2; 
gammas_1 = np.arange(0, 2*np.pi, s)
betas_1 = np.arange(0, np.pi, s)
gammas_2 = np.arange(0, 2*np.pi, s)
betas_2 = np.arange(0, np.pi, s)
exp_costs = np.zeros((len(gammas_1), len(betas_1), len(gammas_2), len(betas_2)))

print('Running simulations...')
for i in tqdm(range(len(gammas_1)), desc="Loop i", position=0):
    for j in tqdm(range(len(betas_1)), desc="Loop j", position=1):
        for k in range(len(gammas_2)):
            for l in range(len(betas_2)):
                gamma = [gammas_1[i], gammas_2[k]]
                beta = [betas_1[j], betas_2[l]]
                exp_costs[i,j,k,l] = expected_cost(J, h, const, TrJ, gamma, beta, costs)

min_cost = np.amin(exp_costs)
i, j, k, l = np.where(exp_costs == min_cost)
i, j, k, l = i[0], j[0], k[0], l[0]
print(f'Best angles: ([{gammas_1[i]}, {gammas_2[k]}], [{betas_1[j]}, {betas_2[l]}])')
print('Minimum average cost for best angels:', min_cost)

#Optimal value for [1 1] and 2
expected_cost(J, h, const, TrJ, [2.8, 3.4], [1.8, 2.4], costs, histogram=True)
run_simulation(J, h, const, B, TrJ, [2.8, 3.4], [1.8, 2.4], shots=1000000, histogram=True)/B

#%% Testing decode function for integer bin packing
decode_integer_bin_packing(W, W_max, '00000000')
