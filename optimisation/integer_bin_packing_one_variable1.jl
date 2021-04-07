using JuMP, Gurobi

# Weights
W = [3, 5, 6, 7, 2]
# Max weight
W_max = 10
I = length(W)

b = [zeros(I); ones(I)]
S = zeros(2*I, W_max*I+I*I)

for r in 1:I
    j = r-1
    for i in I*(W_max+j)+1:I*(W_max+j+1)
        S[r, i] = W[i-I*(W_max+j)]
    end
    for i in W_max*j+1:W_max*(j+1)
        S[r, i] = -(i-W_max*j)
    end
end

for r in I+1:2*I
    j = r-I
    for i in 1:I
        S[r, W_max*I+(i-1)*I+j] = 1
    end
end

m = Model(Gurobi.Optimizer)
@variable(m, x[1:W_max*I+I*I], Bin)
#@objective(m, Min, sum(x[i] for i in 1:W_max*I))
@objective(m, Min, sum(sum(x[i+j*W_max] for i in 1:W_max)^2 for j in 0:I-1))
@constraint(m, [j in 1:2*I], sum(S[j,i]*x[i] for i in 1:W_max*I+I*I) == b[j])

optimize!(m)

if termination_status(m) == MOI.OPTIMAL
    println("z = ", objective_value(m))
    println("Optimal Solutions:")
    println("x = ", value.(x))
end
