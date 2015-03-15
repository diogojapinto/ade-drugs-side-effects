"""
	Uses the latent factors algorithm to predict new drugs adrs

	Elements: drugs
	Features: ADRs (next increment: main quemical structures)
"""

import pickle as pk
import adrecs_interface as ai
from utils import get_training_and_test_sets
from sys import argv
import latent_factors_utils as lf
import pandas
from constants import MAX_TO_KEEP, MIN_TO_KEEP, NR_ITERATIONS
import numpy as np
import scipy as sp

def main():
    """ Entry function.
        When computation is too long, saves objects to files"""

    testing = False

    if len(argv) > 1 and argv[1] == 'test':
        testing = True

    try:
        matrix_df = pk.load(open('data/bipartite_df.p', 'rb'))
    except FileNotFoundError:
        matrix_df = ai.get_drug_adr_matrix()
        pk.dump(matrix_df, open('data/bipartite_df.p', 'wb'))

    # get the training and test sets

    if testing:
        matrix_df, test_set = get_training_and_test_sets(matrix_df)

    # retrieve the numpy matrix, drugs names and adrs names
    matrix = matrix_df.as_matrix()
    drugs = matrix_df.index.values.tolist()
    adrs = matrix_df.columns.values.tolist()

    # compute the svd
    u_mat, s_array, v_mat = lf.compute_svd(matrix)

    # remove the unuseful lines
    u_mat, s_array, v_mat = lf.reduce_singular_values(u_mat, s_array, v_mat)

    # confirm the RMSE
    preliminary_rmse = lf.compute_rmse(matrix, lf.reconstruct_matrix(u_mat, v_mat, s_array))
    print("RMSE after reducing dimension: %d" % (preliminary_rmse))

    # scale the matrixes and perform gradient descent on it
    p_mat, q_mat = lf.get_scaled_matrices(u_mat, s_array, v_mat)
    p_mat, q_mat = lf.gradient_descent(matrix, p_mat, q_mat, testing)

    # test things out
    test_latent_factors(q_mat, test_set)

    # Return the matrixes with the corresponding indexes
    u_df = pandas.DataFrame(p_mat, index=drugs)
    v_df = pandas.DataFrame(q_mat.transpose(), index=adrs)

    return u_df, v_df

def test_latent_factors(q_mat, test_set):
    """ Computes the average error of the obtained latent factors model
        based on the average root_mean_square error of the test_set """
    errors = []
    test_set = test_set.as_matrix()

    for _ in range(NR_ITERATIONS):
        line_i = np.random.randint(0, len(test_set))
        original_obj = test_set[line_i]
        obj = original_obj.copy


        # put some of them in 0
        zeroed_elems_ratio = (MAX_TO_KEEP - MIN_TO_KEEP) * np.random.random_sample() + MIN_TO_KEEP
        candidates = obj > 0

        for index, elem in enumerate(candidates):
            if elem == False:
                continue
            prob = np.random.random_sample()
            if prob <= zeroed_elems_ratio:
                obj[index] = 0

        obj_factors = obj.dot(q_mat.transpose())
        new_obj = obj_factors.dot(q_mat)

        errors.append(lf.compute_rmse(original_obj, new_obj))

    print("Mean : {0:8.6f}".format(sp.mean(errors)))
    print("Minimum : {0:8.6f}".format(min(errors)))
    print("Maximum : {0:8.6f}".format(max(errors)))
    print("Variance : {0:8.6f}".format(sp.var(errors)))
    print("Std. deviation : {0:8.6f}".format(sp.std(errors)))


if __name__ == "__main__":
    main()


"""
funcoes a implementar:
    calcular distância entre drugs (cosine distance entre drug * adr2concept)
    calcular distância entre adrs (cosine distance entre adr * drug2concept)

    cluster de adrs (baseado no cosine distance dos concepts(k-means, k=nº de adrs pode resolver isto))
    cluster de drugs (baseado no cosine distance dos concepts(k-means, k=nº de drugs pode resolver isto))

    prever adrs de drugs (drug * adr2concept * adr2concept^T)
    prever drugs que têm uma dada adr (adr * drug2concept * drug2concept^T)
"""
