import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm 
import random as rnd
from exact_cover_pontus import expectation_value


fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
betas = np.linspace(0,np.pi,100)
gammas = np.linspace(0,np.pi,100)

data=np.zeros((len(betas),len(gammas)))

X, Y = np.meshgrid(betas, gammas)

for i in range(len(betas)):
    for j in range(len(gammas)):
        beta = betas[i]
        gamma = gammas[j]

        data[i][j] = expectation_value(gamma, beta, 10)
        print(str(i) + ':' + str(j)) # debug

print(np.shape(X))
print(np.shape(Y))
print(np.shape(data))
ax.plot_surface(X, Y, data, cmap=cm.coolwarm)
plt.show()
    
