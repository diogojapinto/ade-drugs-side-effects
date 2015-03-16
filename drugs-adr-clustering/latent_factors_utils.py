"""
    Provide all the functionality needed to work with SVD
"""

import pickle as pk
import numpy as np
from constants import (ENERGY_TO_RETAIN, ORIGINAL_ID, REDUCED_ID, IMPROVED_ID, 
                       LEARNING_RATE, REGULARIZATION_PARAM)

def save_to_file(u_mat, s_array, v_mat, identifier):
    """ Saves the SVD components in a file """
    data = [u_mat, s_array, v_mat]
    pk.dump(data, open('data/svd_' + identifier + '.p', 'wb'))

def load_from_file(identifier):
    """ Loads the SVD components from a file """
    data = pk.load(open('data/svd_' + identifier + '.p', 'rb'))
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

def reconstruct_matrix(u_mat, v_mat, s_array=None):
    """ reconstructs the matrix based on the u, s and v provided 
        or on the p and q matrices (u and v scaled) """
    if s_array == None:
        return u_mat.dot(v_mat)
    else:
        return u_mat.dot(get_s_matrix(s_array).dot(v_mat))

def get_scaled_matrices(u_mat, s_array, v_mat):
    """ Computes the scaled U and V matrices based on the Sigma array """
    scaled_u_mat = u_mat.dot(get_s_matrix(np.sqrt(s_array)))
    scaled_v_mat = get_s_matrix(np.sqrt(s_array)).dot(v_mat)

    return scaled_u_mat, scaled_v_mat

def reduce_singular_values(u_mat, s_array, v_mat):
    """ Reduces the dimension of the matrices, retaining at least ENERGY_TO_RETAIN energy """

    # tries to load the reduced matrices
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
        # s_array is ordered in descending order
        min_index = len(s_array)-1

        min_val = s_array[min_index]
        new_energy = sum([x ** 2 for x in s_array]) - min_val ** 2

        if new_energy < base_energy * ENERGY_TO_RETAIN:
            break

        # else delete the corresponding rows and columns
        s_array = np.delete(s_array, min_index)
        u_mat = np.delete(u_mat, min_index, 1)
        v_mat = np.delete(v_mat, min_index, 0)

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

def compute_sse_with_length(original_mat, p_mat, q_mat):
    """ Computes the Sum-of-Squared-Errors """

    new_mat = p_mat * q_mat

    differences_sum = 0
    for original_val, new_val in zip(np.nditer(original_mat), np.nditer(new_mat)):
        differences_sum += (new_val - original_val) ** 2

    p_norms = [x ** 2 for x in np.linalg.norm(p_mat, axis=1)]
    q_norms = [x ** 2 for x in np.linalg.norm(q_mat, axis=0)]


    matrices_lenghts = REGULARIZATION_PARAM * (sum(p_norms) + sum(q_norms))

    return differences_sum + matrices_lenghts

def gradient_descent(original_mat, p_mat, q_mat, testing=False):
    """ Performs Gradient Descent over the reduced SVD matrices """

    # tries to load an existing file
    try:
        p_mat, q_mat = pk.load(open('data/svd_' + IMPROVED_ID + '.p', 'rb'))
        return p_mat, q_mat
    except FileNotFoundError:
        pass

    if testing:
        log_file = open("data/svd.log", 'w')

    counter = 0
    while True:
        new_mat = reconstruct_matrix(p_mat, q_mat)

        diff_matrix = original_mat - new_mat

        p_step = - 2 * diff_matrix.dot(q_mat.transpose()) - 2 * REGULARIZATION_PARAM * p_mat
        q_step = - 2 * p_mat.transpose().dot(diff_matrix) - 2 * REGULARIZATION_PARAM * q_mat

        # break if the steps are too low
        if (np.allclose(np.sum(np.absolute(p_step)), [0]) and 
            np.allclose(np.sum(np.absolute(q_step)), [0])):
            break

        # get the new matrices
        p_mat = p_mat - LEARNING_RATE * p_step
        q_mat = q_mat - LEARNING_RATE * q_step

        counter += 1

        # loging info is very important in ML
        if testing:
            log_file.write("Iteration %d: \t%f\t%f" % (
                counter,
                compute_rmse(original_mat, p_mat.dot(q_mat)), 
                compute_sse_with_length(original_mat, p_mat, q_mat)))

    # save the data
    pk.dump([p_mat, q_mat], open('data/svd_' + IMPROVED_ID + '.p', 'wb'))
    return p_mat, q_mat
