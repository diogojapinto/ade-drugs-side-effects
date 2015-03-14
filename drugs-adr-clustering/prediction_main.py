"""
	Computes the SVD for a given matrix

	Elements: drugs
	Features: ADRs (next increment: main quemical structures)
"""

import pickle as pk
import adrecs_interface as ai
from utils import get_training_and_test_sets
from sys import argv
import svd_utils as svd
import pandas

def main():
    """ Entry function.
        When computation is too long, saves objects to files"""

    TEST_MODE = False

    if len(argv) > 1 and argv[1] == 'test':
        TEST_MODE = True

    try:
        matrix_df = pk.load(open('bipartite_df.p', 'rb'))
    except FileNotFoundError:
        matrix_df = ai.get_drug_adr_matrix()
        pk.dump(matrix_df, open('bipartite_df.p', 'wb'))

    # get the training and test sets

    if TEST_MODE:
        matrix_df, test_set = get_training_and_test_sets(matrix_df)

    # retrieve the numpy matrix, drugs names and adrs names
    matrix = matrix_df.as_matrix()
    drugs = matrix_df.index.values.tolist()
    adrs = matrix_df.columns.values.tolist()

    # compute the svd
    u_mat, s_array, v_mat = svd.compute_svd(matrix)

    # remove the unuseful lines
    u_mat, s_array, v_mat = svd.reduce_singular_values(u_mat, s_array, v_mat)

    # confirm the RMSE
    preliminary_rmse = svd.compute_rmse(matrix, svd.reconstruct_matrix(u_mat, s_array, v_mat))
    print("RMSE after reducing dimension: %d" % (preliminary_rmse))

    # scale the matrixes and perform gradient descent on it
    scaled_u_mat, scaled_v_mat = svd.get_scaled_matrixes(u_mat, s_array, v_mat)
    scaled_u_mat, scaled_v_mat = gradient_descent(scaled_u_mat, scaled_v_mat, TEST_MODE)

    # Return the matrixes with the corresponding indexes
    u_df = pandas.DataFrame(scaled_u_mat, index=drugs)
    v_df = pandas.DataFrame(scaled_v_mat.transpose(), index=adrs)

    return u_df, v_df


if __name__ == "__main__":
    main()
