using JuMP, Gurobi

# Weights
W = [1, 2, 3]
# Max weight
W_max = 3
# Set
I = 1:length(W)
W_ = 1:W_max
m = Model(Gurobi.Optimizer)
@variable(m, x[I,I], Bin)
@variable(m, y[I], Bin)
@objective(m, Min, sum(y[j] for j in I))
@constraint(m, [j in I], sum(W[i]*x[i,j] for i in I) <= W_max*y[j])
@constraint(m, [i in I], sum(x[i,j] for j in I) == 1)

#@objective(m, Min, sum(y[n,j] for j in I for n in W_))
#@variable(m, y[W_,I], Bin)
#@constraint(m, [j in I], sum(W[i]*x[i,j] for i in I) == sum(n*y[n,j] for n in W_))

optimize!(m)

if termination_status(m) == MOI.OPTIMAL
    println("z = ", objective_value(m))
    println("Optimal Solutions:")
    println("x = ", value.(x))
    println("y = ", value.(y))
end
