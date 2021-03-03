from scipy import optimize

def differential_evolution(objective, bounds):
    result = optimize.differential_evolution(objective, bounds)
    return (result.x, result.fun, result)

def shgo(objective, bounds):
    result = optimize.shgo(objective, bounds)
    return (result.x, result.fun, result)

def bruteforce(objective, bounds, max_evaluations=100, plot=False):
    if len(bounds) > 2:
        raise ValueError('This method only work in two dimensions')

    dim = int(np.sqrt(max_evaluations))
    gammas = linspace(bounds[0][0], bounds[0][1], dim)
    betas = linspace(bounds[1][0], bounds[1][1], dim)
    
    result = np.zeros((dim, dim))

    minimum = -1
    minimum_x = []

    for i,gamma in enumerate(gammas):
        for j,beta in enumerate(betas):
            exp_val = objective([gamma, beta])
            result[i][j] = exp_val
            
            if exp_val < minimum or minimum == -1:
                minimum = exp_val
                minimum_x = [gamma, beta]

    if plot:
        print('Plotting not implemented')

    return (minimum_x, minimum, result)


