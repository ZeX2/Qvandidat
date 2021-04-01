import numpy as np

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
def correct_solution(W, W_max, x,y):
    trucks = len(y)
    I = len(W)
    s = 0
    curr_weigh=0
    for i in range(trucks):
        for j in range(I):
            s += y[i][j]   
    if s <= 0:
        print("no truck error")
        return False
    for i in range(I):
        t = 0
        for j in range(I):
            if x[i][j]==1:
                t+=W[curr_weigh]
                curr_weigh+=1             
        if t>W_max:
            print("a truck is carrying to much weight error")
            return False
    return True
def decode_integer_bin_packing(W, W_max, bits):
    I = len(W)
    bits = list(map(int, bits))
    y = bits[:W_max*I]
    result = ""
    weightresult = ""
    curr_weigh=0
    y = np.reshape(y, (-1, I))
    x = bits[W_max*I:]
    x = np.reshape(x, (-1, I))
    if not correct_solution(W, W_max, x, y):
       print("The solution breakes the conditions of the problem")
       return
    trucks = len(y)
    for i in range(trucks):
        for j in range(I):
            if y[i][j] == 1:
                result = result +"Truck "+str(i+1)+ " carries " +str(j+1) +" weights" + "\n"
    result+= "The rest of the trucks do not carry any weight."
    for i in range(I):
        for j in range(I):
            if x[i][j] == 1:
                weightresult += "weight " + str(curr_weigh+1) +", with value "+str(W[curr_weigh])+", is carried by truck " + str(i+1)  +"\n"
                curr_weigh+=1
    print(result)
    print(weightresult)

    