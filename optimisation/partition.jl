using JuMP, Gurobi

S = [3, 3, 4, 5, 6, 10]
S = [3, 3, 4, 4, 1]
S = [3, 1, 1, 2, 2, 1, 3, 2, 2, 1]
S = [4, 5, 13, 8, 3, 6, 3, 25, 4, 10, 8, 12, 8, 9, 7, 5, 6, 7, 10, 11, 4, 2, 5, 3, 10, 9, 12, 13]
I = 1:length(S)

m = Model(Gurobi.Optimizer)
@variable(m, x[I], Bin)
@objective(m, Min, sum(S[i]*(2*x[i]-1) for i in I)^2)
@constraint(m, const1, sum(x[i] for i in I) == length(I)/2)
optimize!(m)

if termination_status(m) == MOI.OPTIMAL
    println("z = ", objective_value(m))
    println("Optimal Solutions:")
    println("x = ", value.(x))
    println("Sum of S1 = ", sum(S[i] for i in I if value.(x[i]) == 1))
    println("Sum of S2 = ", sum(S[i] for i in I if value.(x[i]) == 0))
end
