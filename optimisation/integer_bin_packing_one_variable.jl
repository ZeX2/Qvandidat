using JuMP, Gurobi

# Weights
W = [1, 2, 3]
# Max weight
W_max = 3
I = length(W)

m = Model(Gurobi.Optimizer)
@variable(m, x[1:W_max*I+I*I], Bin)
@objective(m, Min, sum(x[i] for i in 1:W_max*I))
@constraint(m, [j in 0:I-1], sum(W[i-I*(W_max+j)]*x[i] for i in I*(W_max+j)+1:I*(W_max+j+1)) - sum((i-W_max*j)*x[i] for i in W_max*j+1:W_max*(j+1)) == 0)
@constraint(m, [j in 1:I], sum(x[W_max*I+(i-1)*I+j] for i in 1:I) == 1)

optimize!(m)

if termination_status(m) == MOI.OPTIMAL
    println("z = ", objective_value(m))
    println("Optimal Solutions:")
    println("x = ", value.(x))
end
