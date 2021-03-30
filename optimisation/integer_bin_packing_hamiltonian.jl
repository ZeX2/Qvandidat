using JuMP, Gurobi

# Weights
W = [1, 2, 3]
# Max weight
W_max = 3
# Set
I = 1:length(W)
W_ = 0:W_max

A = 1
B = 250
C = 100
m = Model(Gurobi.Optimizer)
@variable(m, x[I,I], Bin)
@variable(m, y[I], Bin)
#@variable(m, u[W_,I], Bin)
#@variable(m, l[I], Bin)
@objective(m, Min, A*sum(y[j] for j in I) +
    B*sum((sum(n*y[j] for n in W_) - sum(W[i]*x[i,j] for i in I))^2 for j in I) +
    C*sum((1 - sum(x[i,j] for j in I)) for j in I)^2)

#B*sum((1-sum(u[n,j] for n in W_))^2 for j in I) +
#@constraint(m, [i in I], sum(x[i,j] for j in I) == 1)
#
#A*(1-sum(l[n] for n in I))^2 +
#A*(sum(n*l[n] for n in I) - sum(y[j] for j in I))^2 +
optimize!(m)
if termination_status(m) == MOI.OPTIMAL
    println("z = ", objective_value(m))
    println("Optimal Solutions:")
    println("x = ", value.(x))
    println("y = ", value.(y))
    #println("u = ", value.(u))
    #println("l = ", value.(l))
end
