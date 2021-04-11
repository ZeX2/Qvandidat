from qiskit import QuantumCircuit
import numpy as np

# if gammas 
def get_circuit(gammas, betas, J, h=None, measure=True):
    if not isinstance(gammas, np.ndarray):
        gammas = np.array([gammas])
        betas = np.array([betas])

    N = len(J)
    p = len(gammas)

    qc = QuantumCircuit(N, N)
    qc.h(range(N))
    qc.barrier()

    for k in range(p):
        gamma = gammas[k]
        beta = betas[k]

        for i in range(N):
            for j in range(i):
                if J[i,j] == 0 or gamma == 0: continue

                qc.cx(i, j)
                qc.rz(2*gamma*J[i,j], j)
                qc.cx(i, j)
                
        if h is None: continue

        for i in range(N):
            if h[i] == 0 or gamma == 0: continue
            qc.rz(2 * gamma * h[i], i)

        qc.barrier()

        if beta == 0: continue
        qc.rx(2*beta, range(N))

    if measure: qc.measure(range(N),range(N))

    return qc

