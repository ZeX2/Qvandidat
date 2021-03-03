from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pickle
import scipy.io


def differential_evolution(objective, bounds, save_file=None):
    result = optimize.differential_evolution(objective, bounds)

    if save_file:
        scipy.io.savemat(save_file + '.mat', result)

    return (result.x, result.fun, result)


def shgo(objective, bounds, save_file=None):
    result = optimize.shgo(objective, bounds)

    if save_file:
        scipy.io.savemat(save_file + '.mat', result)

    return (result.x, result.fun, result)


def bruteforce(objective, bounds, max_evaluations=100, plot=False, save_file=None):
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

    if save_file:
        c = {'betas': betas, 'gammas': gammas,
             'results': result}
        scipy.io.savemat(save_file + '.mat', c)

    return (minimum_x, minimum, result)
