from qiskit import QuantumCircuit
import numpy as np

# if gammas 
def get_circuit(gammas, betas, J, h):
    if not isinstance(gammas, np.ndarray):
        gammas = np.array([gammas])
        betas = np.array([betas])

    N = len(J)
    p = len(gammas)

    qc = QuantumCircuit(N, N)
    qc.h(range(N))

    for k in range(p):
        gamma = gammas[k]
        beta = betas[k]

        for i in range(N):
            for j in range(i):
                qc.cx(i, j)
                qc.rz(2*gamma*J[i,j], j)
                qc.cx(i, j)

        qc.rx(2*beta, range(N))

    qc.measure(range(N),range(N))

    return qc



