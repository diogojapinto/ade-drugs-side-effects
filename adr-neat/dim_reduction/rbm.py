"""
    Utilities for computing and managing Restricted-Boltzman-Machine computations
"""

from numpy import linalg
from sklearn.neural_network import BernoulliRBM
from config import ENERGY_TO_RETAIN

def compute_rbm(matrix):
    """ Computes the RBM for the given (numpy) matrix """

    rank = linalg.matrix_rank(matrix)
    nr_hidden_components = rank*ENERGY_TO_RETAIN

    model = BernoulliRBM(n_components=nr_hidden_components)
    model.fit(matrix)

    return model.transform(matrix)
