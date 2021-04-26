from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.io


def differential_evolution(objective, bounds):
    result = optimize.differential_evolution(objective, bounds)

    return (result.x, result.fun, result)


def shgo(objective, bounds):
    result = optimize.shgo(objective, bounds, iters=5)

    return (result.x, result.fun, result)


def bruteforce(objective, bounds, max_evaluations=100, plot=False):
    if len(bounds) > 2:
        raise ValueError('This method only work in two dimensions')

    dim = int(np.sqrt(max_evaluations))

    gammas = np.linspace(bounds[0][0], bounds[0][1], dim)
    betas = np.linspace(bounds[1][0], bounds[1][1], dim)

    result = np.zeros((dim, dim))

    minimum = -1
    minimum_x = []

    for i, gamma in enumerate(gammas):
        for j, beta in enumerate(betas):
            exp_val = objective(np.array([gamma, beta]))
            result[i][j] = exp_val

            if exp_val < minimum or minimum == -1:
                minimum = exp_val
                minimum_x = [gamma, beta]

    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        X, Y = np.meshgrid(betas, gammas)

        ax.plot_surface(X, Y, result, cmap=cm.coolwarm)
        ax.invert_yaxis()
        plt.show()

    c = {'betas': betas, 'gammas': gammas,
         'results': result}

    return (minimum_x, minimum, c)
