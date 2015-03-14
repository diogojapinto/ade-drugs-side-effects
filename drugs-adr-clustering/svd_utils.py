"""
    Provide all the functionality needed to work with SVD
"""

import pickle as pk
import numpy as np
from constants import (ENERGY_TO_RETAIN, ORIGINAL_ID, REDUCED_ID, IMPROVED_ID, 
                       GRADIENT_DESCENT_LAMBDA, REGULARIZATION_PARAMETER)

def save_to_file(u_mat, s_array, v_mat, identifier):
    """ Saves the SVD components in a file """
    data = [u_mat, s_array, v_mat]
    pk.dump(data, open('svd' + identifier + '.p', 'wb'))

def load_from_file(identifier):
    """ Loads the SVD components from a file """
    data = pk.load(open('svd' + identifier + '.p', 'rb'))
    return data[0], data[1], data[2]

def compute_svd(matrix):
    """ Computes the SVD if it isn't yet computed """
    try:
        u_mat, s_array, v_mat = load_from_file(ORIGINAL_ID)
    except FileNotFoundError:
        u_mat, s_array, v_mat = np.linalg.svd(matrix, full_matrices=False)
        save_to_file(u_mat, s_array, v_mat, ORIGINAL_ID)
    return u_mat, s_array, v_mat

def get_s_matrix(s_array):
    """ returns the diagonal matrix constructed from s(igma) """
    return np.diag(s_array)

def reconstruct_matrix(u_mat, s_array, v_mat):
    """ reconstructs the matrix based on the u, s and v provided """
    return u_mat * get_s_matrix(s_array) * v_mat

def get_scaled_matrixes(u_mat, s_array, v_mat):
    """ Computes the scaled U and V matrixes based on the Sigma array """
    scaled_u_mat = u_mat * get_s_matrix(s_array)
    scaled_v_mat = get_s_matrix(s_array) * v_mat

    return scaled_u_mat, scaled_v_mat

def reduce_singular_values(u_mat, s_array, v_mat):
    """ Reduces the dimension of the matrixes, retaining at least ENERGY_TO_RETAIN energy """

    # tries to load the reduced matrixes
    try:
        u_mat, s_array, v_mat = load_from_file(REDUCED_ID)
        return u_mat, s_array, v_mat
    except FileNotFoundError:
        pass

    u_mat = u_mat.copy()
    s_array = s_array.copy()
    v_mat = v_mat.copy()

    base_energy = sum([x ** 2 for x in s_array])

    while True:
        min_val = min(s_array)
        new_energy = sum([x ** 2 for x in s_array]) - min_val ** 2

        if new_energy < base_energy * ENERGY_TO_RETAIN:
            break

        # else delete the corresponding rows and columns
        min_index = np.where(s_array == min(s_array))[0]
        np.delete(s_array, min_index)
        np.delete(u_mat, min_index, 1)
        np.delete(v_mat, min_index, 0)

    save_to_file(u_mat, s_array, v_mat, REDUCED_ID)

    return u_mat, s_array, v_mat

def compute_rmse(original_mat, new_mat):
    """ Computes the Root-Mean-Squared-Error 
        (What is minimized is the Sum-Squared-Errors) """

    if original_mat.shape != new_mat.shape:
        raise Exception()

    differences_sum = 0

    for original_val, new_val in zip(np.nditer(original_mat), np.nditer(new_mat)):
        differences_sum += (new_val - original_val) ** 2

    result = np.sqrt(differences_sum) / (original_mat.shape[0] * original_mat.shape[1])
    return result

def compute_sse_with_length(original_mat, u_mat, v_mat):
    """ Computes the Sum-of-Squared-Errors """

    new_mat = u_mat * v_mat

    differences_sum = 0
    for original_val, new_val in zip(np.nditer(original_mat), np.nditer(new_mat)):
        differences_sum += (new_val - original_val) ** 2

    return differences_sum + matrixes_lenghts


def gradient_descent(original_mat, u_mat, v_mat, testing=False):
    """ Performs Gradient Descent over the reduced SVD matrixes """


