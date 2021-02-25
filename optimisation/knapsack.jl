using JuMP, GLPK

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

m = Model(GLPK.Optimizer)
@variable(m, x[I], Bin)
@constraint(m, weight_const, sum(x[i] * W[i] for i in I) <= W_max)
@objective(m, Max, sum(x[i] * V[i] for i in I))
optimize!(m)

println("z = ", objective_value(m))
println("Optimal Solutions:")
println("x = ", value.(x))
println("Max weight = ", sum(value.(x[i]) * W[i] for i in I))
