using JuMP, Gurobi, LinearAlgebra

m = Model(Gurobi.Optimizer)

S = [3, 3, 4, 5, 6, 100]
S = [3, 3, 4, 4]
S = [3, 1, 1, 2, 2, 1, 3, 2, 2, 1]
S = [0.1, 0.1, 0.1, 10]
I = 1:length(S)
B = 1
A = (B*maximum(S))^2 + 1

TrJij = (length(S)*A+B*tr(S'*S))
@variable(m, x[I], Bin)
#@objective(m, Min, A*sum(2x[i]-1 for i in I)^2 + B*sum(S[i]*(2x[i]-1) for i in I)^2)
#@objective(m, Min, sum((A+B*S[i]*S[j])*(2x[i]-1)*(2x[j]-1) for j in I, i in I))
@objective(m, Min, 2*sum((A+B*S[i]*S[j])*(2x[i]-1)*(2x[j]-1) for j in I, i in 1:j-1) + TrJij)


optimize!(m)

if termination_status(m) == MOI.OPTIMAL
    println("z = ", objective_value(m))
    println("Optimal Solutions:")
    println("x = ", value.(x))
    println("Sum of S1 = ", sum(S[i] for i in I if value.(x[i]) == 1))
    println("Sum of S2 = ", sum(S[i] for i in I if value.(x[i]) == 0))
end
