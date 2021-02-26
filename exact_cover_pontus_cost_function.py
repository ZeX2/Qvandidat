def cost_function(x1, x2):
    j_12 = 1/2
    h_1 = 1/2
    s1 = 1 - 2*x1
    s2 = 1 - 2*x2

    return j_12*s1*s2 + h_1*s1 + 1
