import numpy as np

def integer_bin_packing(W, W_max, A = None, B = None, C = None): 
    # C >> A >> B
    I = len(W)
    N =  W_max*I+I*I
    b = np.concatenate((np.zeros(I), np.ones(I)))
    M = len(b)
    S = np.zeros((M, N))
    c = np.zeros((N, N))
    
    for r in range(1, I+1):
        j = r-1
        for i in range(I*(W_max+j)+1, I*(W_max+j+1)+1):
            S[r-1, i-1] = W[i-I*(W_max+j)-1]
        for i in range(W_max*j+1, W_max*(j+1)+1):
            S[r-1, i-1] = -(i-W_max*j)
    
    for r in range(I+1, 2*I+1):
        j = r-I
        for i in range(1, I+1):
            S[r-1, W_max*I+(i-1)*I+j-1] = 1
    
    
    for j in range(1, I+1):
        for i in range(W_max*(j-1)+1, W_max*j+1):
            c[j-1, i-1] = 1

    if not (A or B or C):
        B_upper = sum(sum(max(c[j,i], 0) for i in range(N))**2 for j in range(N))
        A_lower = min(min(np.abs(S[j,np.nonzero(S[j,:])[0]])) for j in range(M//2))**2
        A_lower = min(min(np.abs(S[j,np.nonzero(S[j,:])[0]])) for j in range(M//2))
        A_upper = sum(max(abs(b[j]-sum(max(S[j,i], 0) for i in range(N))),
                          abs(b[j]-sum(min(S[j,i], 0) for i in range(N))))**2 for j in range(M//2))
        C_lower = min(min(np.abs(S[j,np.nonzero(S[j,:])[0]])) for j in range(M//2, M))**2
        B = 4
        A = int(B*max(np.ceil(B_upper/A_lower), 2))
        C = int(A*max(np.ceil(A_upper/C_lower), 1.5))

    J = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            J[i, j] = A*sum(S[k, i]*S[k, j] for k in range(M//2))/4
            J[i, j] += C*sum(S[k, i]*S[k, j] for k in range(M//2, M))/4
            J[i, j] += B*sum(c[k, i]*c[k, j] for k in range(N))/4
    
    h = np.zeros(N)
    for i in range(N):
        for j in range(N):
            h[i] += B*sum(c[j, i]*c[j, k] for k in range(N))/2
    
    for i in range(N):
        for j in range(M//2):
            h[i] -= A*S[j, i]*(2*b[j] - sum(S[j, k] for k in range(N)))/2
        for j in range(M//2, M):
            h[i] -= C*S[j, i]*(2*b[j] - sum(S[j, k] for k in range(N)))/2

    const = (B/4)*sum(sum(c[j,i] for i in range(N))**2 for j in range(N))
    for j in range(M//2):
        const += (A/4)*(2*b[j] - sum(S[j,i] for i in range(N)))**2
    for j in range(M//2, M):
        const += (C/4)*(2*b[j] - sum(S[j,i] for i in range(N)))**2

    return J, h, const, A, B, C

def correct_solution(W, W_max, bits):
    W = np.array(W)
    I = len(W)
    bits = list(map(int, bits))
    y = bits[:W_max*I]
    y = np.reshape(y, (-1, W_max))
    x = bits[W_max*I:]
    x = np.reshape(x, (-1, I))
    
    if np.any(np.sum(x, axis=0) != 1):
        return False 
    
    possible_weights = np.array(range(1, W_max+1))
    for i in range(len(W)):
        if np.dot(W, x[i,]) != np.dot(possible_weights, y[i,]):
            return False

    return True   
    
def _correct_solution(W, W_max, x, y):
    if np.any(W > W_max):
        print('Invalid problem! There are items with greater weight than truck capacity.')
        return False

    if np.any(np.sum(y, axis=1) > 1):
        print('Invalid solution! There are trucks with several weights.')
        return False

    if np.sum(y) == 0:
        print('Invalid solution! No trucks used.')
        return False

    if np.any(np.sum(x, axis=0) != 1):
        print('Invalid solution! Each item has to be in one truck and one truck only.')
        return False 
    
    possible_weights = np.array(range(1, W_max+1))
    for i in range(len(W)):
        if np.dot(W, x[i,]) != np.dot(possible_weights, y[i,]):
            print('Invalid solution! The constraint regulating truck weight is not satisfied.')
            return False

    return True

def decode_integer_bin_packing(W, W_max, bits):
    W = np.array(W)
    I = len(W)
    bits = list(map(int, bits))
    y = bits[:W_max*I]
    y = np.reshape(y, (-1, W_max))
    x = bits[W_max*I:]
    x = np.reshape(x, (-1, I))

    if not _correct_solution(W, W_max, x, y): 
        return False

    bins_used = np.sum(y)
    print(f'{bins_used}/{I} trucks used!')
    
    for i in range(I):
        if np.sum(y[i,]) == 1:
            weight = np.where(y[i,] == 1)[0][0] + 1
            contains = W[np.where(x[i,] == 1)[0]]
            print(f'Truck {i+1} has weight {weight} and contains item(s) with weight(s): {contains}')
        else:
            print(f'Truck {i+1} is empty!')
    
    return True
def decode_pure(W,W_max,bits):
    W = np.array(W)
    I = len(W)
    bits = list(map(int, bits))
    y = bits[:W_max*I]
    y = np.reshape(y, (-1, W_max))
    x = bits[W_max*I:]
    x = np.reshape(x, (-1, I))
    bins_used = np.sum(y)
    print(f'{bins_used}/{I} trucks used!')
    
    for i in range(I):
        if np.sum(y[i,]) == 1:
            weight = np.where(y[i,] == 1)[0][0] + 1
            contains = W[np.where(x[i,] == 1)[0]]
            print(f'Truck {i+1} has weight {weight} and contains item(s) with weight(s): {contains}')
        else:
            print(f'Truck {i+1} is empty!')