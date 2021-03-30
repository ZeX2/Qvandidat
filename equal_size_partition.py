import numpy as np

def equal_size_partition(S):
    B = 1
    A = B*max(S)^2 + 1
    S = np.array(S)
    J = A+B*S.reshape(-1,1)*S
    h = np.array([0]*len(S))
    const = 0

    return J, h, const