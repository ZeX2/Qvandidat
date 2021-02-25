from operator import itemgetter

import matplotlib.pyplot as plt
%matplotlib agg
import numpy as np
from qiskit import(
  QuantumCircuit,
  execute,
  Aer)
from qiskit.visualization import plot_histogram
from qiskit_textbook.tools import array_to_latex

backend = Aer.get_backend('unitary_simulator')
simulator = Aer.get_backend('qasm_simulator')

#s = 0.1;
#gamma_ = np.arange(0,2* np.pi, s)
#beta_ = np.arange(0, 2*np.pi, s)
S = np.array([2, 2, 1, 1])
S = np.array([4, 5, 13, 8, 3, 6, 3, 25, 4, 10, 8, 12, 8, 9, 7, 5, 6, 7, 10, 11, 4, 2, 5, 3, 10, 9, 12, 13])
S = np.array([4, 5, 13, 8, 3, 6, 3, 25, 4, 10, 8, 12, 8, 9, 7, 5, 6, 7, 10, 11, 4, 2, 5, 3, 10, 10])
N = len(S)

beta = 1
gamma = np.pi/5
B = 1
A = B*max(S)^2 + 1

J = A+B*S.reshape(-1,1)*S
TrJ = np.trace(J)

# Quantum Circuit
qc = QuantumCircuit(N, N)
qc.h(range(N))
qc.barrier()

for i in range(N):
    for j in range(i-1):
        qc.cx(i, j)
        qc.rz(2*gamma*J[i,j], j)
        qc.cx(i, j)

qc.barrier()
qc.rx(2*beta, range(N))

# Circuit matrix
# Do not run this code if matrix S is large

#unitary = execute(qc, backend).result().get_unitary()
#print(unitary)
#array_to_latex(unitary, pretext="\\text{Circuit = }\n")


# Simulate
qc.measure(range(N),range(N))
job = execute(qc, simulator, shots=1)
result = job.result()
counts = result.get_counts(qc)
print("Counts:", counts)

# Plot results
# Do not run this either if matrix S is large

#plot_histogram(counts)
#qc.draw(output='mpl', filename='circuit') 

# Evaluate cost
bits_to_spins = {bits: [1 if bit == '1' else -1 for bit in bits] for bits in counts.keys()}
costs = dict()

for bits, spins in bits_to_spins.items():
    costs[bits] = 2*sum((A + B*S[i]*S[j])*spins[i]*spins[j] for i in range(N) for j in range(i)) + TrJ

print("Costs:", costs)
print("Minimal cost:", min(costs.items(), key=itemgetter(1)))