from scipy import optimize

def nelder_mead(objective, x0):
    result = optimize.minimize(objective, x0, method='nelder-mead')
    return (result.x, result.fun, result)

