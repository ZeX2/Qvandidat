def depolarizing_probability(fidelity, d=2):
    return 3/4*(1 - (fidelity - 1/d)/(1 - 1/d))
