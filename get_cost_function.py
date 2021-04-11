import numpy as np 

# spins is a list of spins, first spin correspond to first qubit
# spins and J are both of type np.array

def get_cost_function(J, h=None, const=0):
    if h is None:
        h = np.zeros(len(J))

    def cost_function(spins):
        spins = np.array(spins)
        SS = spins.reshape(-1,1)*spins # spin^T * spin
        N = len(spins)

        # elementwise multuplication, tril(.., -1) lower triangle wo/ diagonal
        return 2 * sum(sum(np.tril(J, -1) * SS))  \
                    + np.trace(J) \
                    + h.dot(spins) \
                    + const

    return cost_function

def proof_of_equal_cost_functions():
    def cost_function(spins, J, h, const):

        TrJ = np.trace(J)
        N = len(J)
        cost = TrJ + const
        cost += 2*sum((J[i,j]*spins[i]*spins[j] for i in range(N) for j in range(i)))
        cost += sum(h[i]*spins[i] for i in range(N))
        
        return cost

    def integer_bin_packing(W, W_max, A = 2, B = 1): 
        # A > B
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

        J = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                J[i, j] = A*sum(S[k, i]*S[k, j] for k in range(M))/4
                J[i, j] += B*sum(c[k, i]*c[k, j] for k in range(N))/4
        
        h = np.zeros(N)
        for i in range(N):
            for j in range(N):
                h[i] += B*sum(c[j, i]*c[j, k] for k in range(N))/2
        
        for i in range(N):
            for j in range(M):
                h[i] -= A*S[j, i]*(2*b[j] - sum(S[j, k] for k in range(N)))/2
        
        const = (B/4)*sum(sum(c[j,i] for i in range(N))**2 for j in range(N))
        for j in range(M):
            const += (A/4)*(2*b[j] - sum(S[j,i] for i in range(N)))**2

        return J, h, const


    while True:
        
        W = np.random.randint(1, 3, np.random.randint(1, 3))
        W_max = np.max(W)
        A = np.random.randint(1, 3)
        B = np.random.randint(1, 3)

        J, h, const = integer_bin_packing(W, W_max, A, B)
        
        cost_function2 = get_cost_function(J, h, const)
        
        spins = 2 * np.random.randint(0, 1, h.shape) - 1
        bit_str = ['1' if spin == 1 else '0' for spin in spins]
        
        cost_2 = cost_function2(spins)
        cost_1 = cost_function(spins, J, h, const)
        
        print(cost_2 == cost_1, cost_2, cost_1)

