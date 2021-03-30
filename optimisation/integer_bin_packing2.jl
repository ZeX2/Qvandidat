using JuMP, Gurobi

# Weights
W = [1, 2, 3]
# Max weight
W_max = 3
# Set
I = 1:length(W)
W_ = 1:W_max

N = 1:(length(W)*W_max+length(W)^2)
m = Model(Gurobi.Optimizer)

A = 10
B = 1
# H_B: @objective(m, Min, sum(y[n,j] for j in I for n in W_))
# First length(W)*W_max variables in N are for y[n,j]
# Last length(W)*length(W) variables in N are for x[i,j]

# H_A: @constraint(m, [j in I], sum(W[i]*x[i,j] for i in I) == sum(n*y[n,j] for n in W_))
# + @constraint(m, [i in I], sum(x[i,j] for j in I) == 1)
# So length(b) = 2*length(W)
b = [zeros(length(W)); ones(length(W))]

# Matris S
# length(b) antal rader
# length(N) antal kolumner
S = zeros(length(b), length(N))
for i in 1:length(W)
    for n in 1:W_max
        S[i,n] = -n
    end
    #for j in W_max
end
