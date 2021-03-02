import numpy as np

# S is an np.array
def get_ising_model(S):
    B = 1
    A = B*max(S)^2 + 1

    SS = S.reshape(-1,1)*S # S^T * S

    J = A+B*SS
    h = 0

    return (J, h, (0,2 *np.pi))
