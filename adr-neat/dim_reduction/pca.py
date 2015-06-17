"""
    Utilities for computing and managing Principal-Component-Analysis computations
"""

from numpy import linalg
from sklearn.decomposition import PCA
from sklearn import preprocessing
from config import ENERGY_TO_RETAIN

def compute_pca(matrix):
    """ Computes the PCA for the given (numpy) matrix """

    rank = linalg.matrix_rank(matrix)
    nr_hidden_components = rank*ENERGY_TO_RETAIN

    model = PCA(n_components=nr_hidden_components)
    model.fit(matrix)

    values = model.transform(matrix)

    # Remove if not needed
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    values = min_max_scaler.fit_transform(values)

    return values
