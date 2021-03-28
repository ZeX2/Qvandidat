import numpy as np 

# spins is a list of spins, first spin correspond to first qubit
# spins and J are both of type np.array
def get_cost_function(J, h, S):

    def cost_function(spins):
        spins = np.array(spins)
        SS = spins.reshape(-1,1)*spins # spin^T * spin
        N = len(spins)

        # elementwise multuplication, tril(.., -1) lower triangle wo/ diagonal
        return 2 * sum(sum(np.tril(J, -1) * SS)) + np.trace(J)

    return cost_function
