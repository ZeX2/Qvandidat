import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm 
import random as rnd
from expectation_value_cirq import expectation_value as expectation_value_cirq
from expectation_value_qiskit import expectation_value as expectation_value_qiskit


def plot_expectation_value(resolution_steps, repetitions, expectation_value_impl):
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    betas = np.linspace(0,np.pi,resolution_steps)
    gammas = np.linspace(0,np.pi,resolution_steps)

    data=np.zeros((len(betas),len(gammas)))

    X, Y = np.meshgrid(betas, gammas)

    for i in range(len(betas)):
        for j in range(len(gammas)):
            beta = betas[i]
            gamma = gammas[j]

            data[i][j] = expectation_value_impl(gamma, beta, repetitions)
            print(str(i) + ':' + str(j)) # debug

    ax.plot_surface(X, Y, data, cmap=cm.coolwarm)
    ax.invert_yaxis()
    plt.show()

    fig, ax = plt.subplots()
    ax.contour(X, Y, data)
    plt.show()

plot_expectation_value(10, 10, expectation_value_cirq)
#plot_expectation_value(100, 100, expectation_value_qiskit)

