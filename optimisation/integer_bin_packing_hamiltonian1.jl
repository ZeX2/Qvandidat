using JuMP, Gurobi

# Weights
W = [1, 2, 3]
# Max weight
W_max = 3
# Set
I = 1:length(W)
W_ = 1:W_max
A = 1
B = 200
C = 30
m = Model(Gurobi.Optimizer)
@variable(m, x[I,I], Bin)
@variable(m, y[W_,I], Bin)
@objective(m, Min, A*sum(y[n,j] for n in W_ for j in I)^2 +
    #B*sum((1-sum(y[n,j] for n in W_))^2 for j in I) +
    C*sum((sum(n*y[n,j] for n in W_) - sum(W[i]*x[i,j] for i in I))^2 for j in I) +
    C*sum((1 - sum(x[i,j] for j in I)) for i in I)^2)

optimize!(m)
if termination_status(m) == MOI.OPTIMAL
    println("z = ", objective_value(m))
    println("Optimal Solutions:")
    println("x = ", value.(x))
    println("y = ", value.(y))
    #println("u = ", value.(u))
    #println("l = ", value.(l))
end
