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
J, h, const, A, B = integer_bin_packing(W, W_max)
TrJ = np.trace(J)

bits_list = get_bits_list(len(J))
costs = {bits: cost_function(bits, J, h, const, TrJ)/B for bits in bits_list}

#%% Equal Size Partition
# S = [1, 2, 3, 4]
# J, h, const = equal_size_partition(S)
# TrJ = np.trace(J)

#%% Optimization
p = 2 #Sets the p-level
out = True #Set this to True to have continous update on the optimization
angles, cost = optimize_angles(p, J, h, const, TrJ, costs, out=out)
print(angles)
print(cost)

expected_cost(J, h, const, TrJ, 5.71620769, 0.39746979, costs, histogram=True)/B
expected_cost(J, h, const, TrJ, [6.06563229, 1.59990683], [4.64982907, 0.79812301], costs, histogram=True)/B
expected_cost(J, h, const, TrJ, [2.17174197, 2.63865832], [4.79224862, 2.38503763], costs, histogram=True)/B

#%% Run simulation for several (gamma, beta) where p = 1
plt.switch_backend("TkAgg")
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
        exp_costs[i,j] = expected_cost(J, h, const, TrJ, gammas[i], betas[j], costs)/B

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

#Optimal value for [1 1] and 1
expected_cost(J, h, const, TrJ, 4, 0.8, costs, histogram=True)/B
run_simulation(J, h, const, TrJ, 4, 0.8, shots=1000000, histogram=True)/B

#Optimal value for [1 1] and 2
expected_cost(J, h, const, TrJ, 5.9, 0.4, costs, histogram=True)/B
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
                exp_costs[i,j,k,l] = expected_cost(J, h, const, TrJ, gamma, beta, costs)/B

min_cost = np.amin(exp_costs)
i, j, k, l = np.where(exp_costs == min_cost)
i, j, k, l = i[0], j[0], k[0], l[0]
print(f'Best angles: ([{gammas_1[i]}, {gammas_2[k]}], [{betas_1[j]}, {betas_2[l]}])')
print('Minimum average cost for best angels:', min_cost)


#Optimal value for [1 1] and 2
expected_cost(J, h, const, TrJ, [2.8, 3.4], [1.8, 2.4], costs, histogram=True)/B
run_simulation(J, h, const, B, TrJ, [2.8, 3.4], [1.8, 2.4], shots=1000000, histogram=True)/B

#%% Testing decode function for integer bin packing
decode_integer_bin_packing(W, W_max, '00000000')
