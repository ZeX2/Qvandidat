using JuMP, Gurobi

# Weights
W = [3,3,3]
# Max weight
W_max = 8
# Set
I = 1:length(W)
W_ = 1:W_max
m = Model(Gurobi.Optimizer)
@variable(m, x[I,I], Bin)
@variable(m, y[W_,I], Bin)
@objective(m, Min, sum(sum(y[n,j] for n in W_)^2 for j in I ))
@constraint(m, [i in I], sum(x[i,j] for j in I) == 1)
@constraint(m, [j in I], sum(W[i]*x[i,j] for i in I) == sum(n*y[n,j] for n in W_))

optimize!(m)

if termination_status(m) == MOI.OPTIMAL
    println("z = ", objective_value(m))
    println("Optimal Solutions:")
    println("x = ", value.(x))
    println("y = ", value.(y))
end
