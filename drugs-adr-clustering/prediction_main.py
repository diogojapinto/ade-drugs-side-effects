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
    test_latent_factors(q_mat, )

    # Return the matrixes with the corresponding indexes
    u_df = pandas.DataFrame(p_mat, index=drugs)
    v_df = pandas.DataFrame(q_mat.transpose(), index=adrs)

    return u_df, v_df


if __name__ == "__main__":
    main()
