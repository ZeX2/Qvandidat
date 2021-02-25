using JuMP, Gurobi

#set_optimizer_attribute(model, "tm_lim", 60 * 1_000)
#set_optimizer_attribute(model, "msg_lev", GLPK.GLP_MSG_OFF)

# Weights
W = [1, 2, 5, 7, 1, 4, 5, 9, 10]
# Values
V = [1, 6, 9, 10, 4, 6, 10, 10, 11]
# Max weight
W_max = 25
# Set
I = 1:length(W)
N = 1:W_max
B = 10
A = B*maximum(V) + 10
println(B, A)

m = Model(Gurobi.Optimizer)
@variable(m, x[I], Bin)
@variable(m, y[N], Bin)
@objective(m, Min, A*(1-sum(y[n] for n in N))^2 + A*(sum(n*y[n] for n in N) - sum(x[i]*W[i] for i in I))^2 - B*sum(x[i]*V[i] for i in I))
optimize!(m)

println("z = ", objective_value(m))
println("Optimal Solutions:")
println("x = ", value.(x))
println("Max weight = ", sum(value.(x[i])*W[i] for i in I))
