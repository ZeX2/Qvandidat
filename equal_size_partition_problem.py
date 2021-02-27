from operator import itemgetter

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
%matplotlib agg

from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
from qiskit_textbook.tools import array_to_latex

from scipy import signal
BACKEND = Aer.get_backend('unitary_simulator')
SIMULATOR = Aer.get_backend('qasm_simulator')

def run_simulation(J, TrJ, beta, gamma, shots=1000, output=True, draw=True):
    # Quantum Circuit
    N = len(J)
    qc = QuantumCircuit(N, N)
    qc.h(range(N))
    qc.barrier()
    
    for i in range(N):
        for j in range(i):
            qc.cx(i, j)
            qc.rz(2*gamma*J[i,j], j)
            qc.cx(i, j)
    
    qc.barrier()
    qc.rx(2*beta, range(N))
    
    # Circuit matrix
    # Do not run this code if matrix S is large
    
    #unitary = execute(qc, BACKEND).result().get_unitary()
    #print(unitary)
    #array_to_latex(unitary, pretext='\\text{Circuit = }\n')

    # Simulate
    qc.measure(range(N), range(N))
    job = execute(qc, SIMULATOR, shots=shots)
    result = job.result()
    counts = result.get_counts(qc)

    # Plot results
    # Do not run this either if matrix S is large
    if draw:
        plot_histogram(counts)
        qc.draw(output='mpl', filename='circuit') 
    
    # Evaluate cost
    bits_to_spins = {bits: [1 if bit == '1' else -1 for bit in bits] for bits in counts.keys()}
    costs = dict()
    
    for bits, spins in bits_to_spins.items():
        costs[bits] = 2*sum((A + B*S[i]*S[j])*spins[i]*spins[j] for i in range(N) for j in range(i)) + TrJ
    
    avg_cost = sum([count*cost for count, cost in zip(counts.values(), costs.values())])/shots

    if output:
        print('Counts:', counts)
        print('Costs:', costs)
        print('Average cost:', avg_cost)
        min_cost = min(costs.values())
        min_bits = [bits for bits, cost in costs.items() if cost == min_cost]
        print('Minimal cost:', min_cost)
        print('Bits for minimal cost:', min_bits)

    return avg_cost

# Run simulation for one pair of (gamma, beta)
S = np.array([1, 2, 3, 4, 7, 7])
#S = np.array([4, 5, 13, 8, 3, 6, 3, 25, 4, 10, 8, 12, 8, 9, 7, 5, 6, 7, 10, 11, 4, 2, 5, 3, 10, 9, 12, 13])
S = np.array([4, 5, 13, 8, 3, 6, 3, 25, 4, 10, 8, 12, 8, 9, 7, 5, 6, 7, 10, 11, 4, 2, 5, 3, 10, 10])
B = 1
A = B*max(S)^2 + 1

beta = 2.75
gamma = 1.3
J = A+B*S.reshape(-1,1)*S
TrJ = np.trace(J)

run_simulation(J, TrJ, beta, gamma, shots=1, draw=False)

quit()
# Run simulation for several (gamma, beta)
s = 0.05; 
gammas = np.arange(0, np.pi, s)
betas = np.arange(0, np.pi, s)
avg_costs = np.zeros((len(betas), len(gammas)))

print('Running simulations...')
for i in range(len(betas)):
    for j in range(len(gammas)):
        avg_costs[i,j] = run_simulation(J, TrJ, betas[i], gammas[j], shots=3, output=False)

gammas_, betas_ = np.meshgrid(betas, gammas)

fig = plt.figure()
ax  = fig.gca(projection='3d')
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$\gamma$')
ax.set_zlabel('Negative costs')
surf = ax.plot_surface(betas_, gammas_, -1*avg_costs, cmap=cm.coolwarm, linewidth=0, antialiased=True)
#ax.scatter(1.95, 1.05, -16.32, color="k", s=20)
plt.show()

min_cost = np.amin(avg_costs)
i, j = np.where(avg_costs == min_cost)
i, j = i[0], j[0]
print(f'Best angles: ({betas[i]}, {gammas[j]})')
print('Minimum average cost for best angels:', min_cost)

#minimums = signal.argrelextrema(avg_costs, np.less)
#print(minimums)
